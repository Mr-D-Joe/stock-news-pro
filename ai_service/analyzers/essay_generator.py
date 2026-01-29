"""Essay generator with AI-powered analysis."""

from __future__ import annotations

import logging
from typing import Optional, Sequence

from ai_service.analyzers.base_client import BaseAIClient
from ai_service.analyzers.provider_factory import ProviderFactory
from ai_service.config import Settings
from ai_service.models.article import AnalysisResult, ArticleCollection
from ai_service.models.contracts import AnalysisOutput, NewsItem, DeepWebSource, FundamentalsData
from ai_service.pipeline.base import PipelineContext, PipelineStep

logger = logging.getLogger(__name__)


class EssayGenerator(PipelineStep[ArticleCollection, AnalysisResult]):
    """Generate analytical essays from article collections using AI."""

    name = "essay_generator"

    def __init__(
        self,
        settings: Optional[Settings] = None,
        language: Optional[str] = None,
        include_anomaly_analysis: Optional[bool] = None,
        max_articles_for_ai: Optional[int] = None,
    ):
        self.settings = settings or Settings()
        self.language = language or self.settings.default_language
        self.include_anomaly_analysis = (
            include_anomaly_analysis 
            if include_anomaly_analysis is not None 
            else self.settings.enable_anomaly_detection
        )
        self.max_articles_for_ai = max_articles_for_ai or self.settings.max_articles_for_ai
        self._client: Optional[BaseAIClient] = None

    @property
    def client(self) -> BaseAIClient:
        """Lazy-initialize AI client using fallback chain (OpenAI -> Gemini)."""
        if self._client is None:
            # Use fallback client: OpenAI (primary) -> Gemini (secondary)
            self._client = ProviderFactory.get_client("fallback", self.settings)
        return self._client

    def _ensure_client_callbacks(self, context: PipelineContext) -> None:
        """Ensure client is hooked up to context callbacks."""
        client = self.client
        if context.on_wait_start:
            client.on_wait_start = context.on_wait_start
        if context.on_wait_tick:
            client.on_wait_tick = context.on_wait_tick

    def process(
        self, input_data: ArticleCollection, context: PipelineContext
    ) -> AnalysisResult:
        """
        Generate essay from article collection.
        This legacy method adapts the new JSON flow to the old AnalysisResult interface.
        """
        self._ensure_client_callbacks(context)
        
        # Prepare data for new analysis method
        ticker = input_data.query_stocks[0] if input_data.query_stocks else "UNKNOWN"
        language = context.config.language if hasattr(context.config, 'language') else self.language
        
        # Convert articles to summarized strings (proper None handling)
        news_context = [
            f"[{a.source}] {a.title}: {(a.summary or '')[:200]}"
            for a in input_data.articles[:self.max_articles_for_ai]
        ]
        
        # Call the new structured analysis
        data = self.generate_analysis(
            ticker=ticker,
            company_name=ticker, # Fallback, ideally passed in
            language=language,
            news_context=news_context,
            fundamentals=input_data.fundamentals
        )
        
        # Map JSON dict back to AnalysisResult for compatibility
        return AnalysisResult(
            essay=data.get("essay", ""),
            summary=data.get("summary", ""),
            swot=data.get("swot", {}),
            key_findings=data.get("key_findings", []),
            watch_items=data.get("watch_items", []),
            article_collection=input_data,
            fundamentals=input_data.fundamentals,
            metadata={"status": "generated_via_json_mode"}
        )

    def generate_analysis(
        self,
        ticker: str, 
        company_name: str, 
        language: str, 
        news_context: Sequence[NewsItem | str] | None = None,
        fundamentals: FundamentalsData | None = None,
        deep_sources: Sequence[DeepWebSource | str] | None = None
    ) -> AnalysisOutput:
        """
        Generate a complete DeltaValue analysis using AI's built-in knowledge.
        Returns a structured dictionary (JSON).
        Accepts both mainstream news and deep web sources.
        """
        import json
        
        client = self.client # Use the property to ensure initialization
        
        # Build mainstream news section (ALL unique articles with summaries)
        news_section = "No recent mainstream news."
        if news_context:
            # Deduplicate by title (fuzzy match via lowercase strip)
            seen_titles = set()
            unique_items: list[NewsItem | str] = []
            for item in news_context:
                if isinstance(item, dict):
                    title = item.get('title', '').lower().strip()
                    if title and title not in seen_titles:
                        seen_titles.add(title)
                        unique_items.append(item)
                else:
                    unique_items.append(item)
            
            items: list[str] = []
            for item in unique_items:  # ALL unique articles
                if isinstance(item, dict):
                    source = item.get('source', 'News')
                    title = item.get('title', 'Unknown')
                    summary = (item.get('summary') or '')[:300]  # Include summary content
                    if summary:
                        items.append(f"- [{source}] {title}: {summary}")
                    else:
                        items.append(f"- [{source}] {title}")
                else:
                    items.append(f"- {str(item)}")
            news_section = "\\n".join(items)
            logger.info(f"Essay: Using {len(unique_items)} unique news articles (deduplicated from {len(news_context)})")

        # Build Deep Web section (expanded context)
        deep_section = "No deep web sources found."
        if deep_sources:
            deep_items: list[str] = []
            for item in deep_sources:
                if isinstance(item, dict):
                    source = item.get('source', 'DeepWeb')
                    title = item.get('title', 'Doc')
                    url = item.get('url', 'N/A')
                    summary = item.get('summary', '')[:2000]  # 2000 chars for economic content
                    deep_items.append(f"- [DEEP WEB / {source}] {title} ({url}): {summary}")
                else:
                    deep_items.append(f"- [DEEP WEB] {str(item)}")
            deep_section = "\n".join(deep_items)
    
        # Build fundamentals section
        fund_section = ""
        if fundamentals:
            fund_section = f"""
    ## Key Fundamentals:
    - P/E Ratio: {fundamentals.get('pe_ratio', 'N/A')}
    - PEG Ratio: {fundamentals.get('peg_ratio', 'N/A')}
    - ROE: {fundamentals.get('roe', 'N/A')}
    - Debt/Equity: {fundamentals.get('debt_to_equity', 'N/A')}
    - Target Mean Price: {fundamentals.get('target_mean_price', 'N/A')}
    - Analyst Rec: {fundamentals.get('recommendation', 'N/A')}
    - Business Summary: {fundamentals.get('business_summary', 'N/A')[:400]}...
    """
        
        prompt = f"""
        Analyze {company_name} ({ticker}) in {language}.
        Role: Senior Financial Analyst.
        Task: Create an investment memo.
        Output: Return EXACTLY ONE valid JSON object. NOT an array. NO MARKDOWN. NO REPETITION.

        [Fundamentals]
        {fund_section}

        [News Context]
        {news_section}

        [Deep Web Alpha]
        {deep_section}

        JSON Structure:
        {{
            "essay": "Executive analysis (3 paras). 1) Strategy, 2) Financials, 3) Verdict. BE CONCISE. DO NOT REPEAT SENTENCES.",
            "summary": "1 sentence Buy/Hold/Sell decision.",
            "swot": {{
                "strengths": ["3 key strengths"],
                "weaknesses": ["3 key weaknesses"],
                "opportunities": ["3 opportunities"],
                "threats": ["3 risks"]
            }},
            "buffett_view": "Warren Buffett's view (2 sentences).",
            "lynch_view": "Peter Lynch's view (2 sentences).",
            "outlook": "12-month outlook (2 sentences). Highlight Deep Web variances if any.",
            "key_findings": ["5 key facts. Mark deep web sources as '[Deep Web]'."],
            "watch_items": ["3 monitor items"]
        }}
        """
    

    
        try:
            response = client.generate(prompt, temperature=0.3)
            # Extract JSON from response (handle markdown blocks)
            cleaned_response = response.strip()
            if "```json" in cleaned_response:
                cleaned_response = cleaned_response.split("```json")[1].split("```")[0].strip()
            elif "```" in cleaned_response:
                cleaned_response = cleaned_response.split("```")[1].split("```")[0].strip()
                
            # Try direct parse first
            try:
                # strict=False allows control characters like newlines in strings
                data = json.loads(cleaned_response, strict=False)
                
                # Resilience: Ensure valid dict structure (AI sometimes returns list)
                if isinstance(data, list):
                    logger.warning(f"AI returned list instead of dict (Standard Parse). Attempting to recover. (Len: {len(data)})")
                    if len(data) > 0 and isinstance(data[0], dict):
                        data = data[0]
                    else:
                        raise ValueError("JSON is a list, expected dict")

                return data
            except json.JSONDecodeError:
                # Fallback to json_repair for malformed JSON (missing commas, unescaped quotes)
                try:
                    import json_repair
                    data = json_repair.loads(cleaned_response)
                    logger.info("Successfully repaired malformed JSON")
                    
                    # Resilience: Ensure valid dict structure (AI sometimes returns list)
                    if isinstance(data, list):
                        logger.warning(f"AI returned list instead of dict after repair. (Len: {len(data)})")
                        if len(data) > 0 and isinstance(data[0], dict):
                            data = data[0]  # Take first element if it's a valid dict
                        else:
                            # Raise error - don't bypass with str(data)
                            raise ValueError(f"AI returned invalid list structure: {type(data[0] if data else 'empty')}")
                    
                    return data
                except ImportError:
                     logger.error("json_repair module not found. Please install it: pip install json_repair")
                except Exception as e:
                     logger.warning(f"json_repair failed: {e}")

                # If repair failed, look for partial JSON
                logger.error(f"Could not parse JSON from response: {cleaned_response[:500]}...")
                raise ValueError("No JSON found")
        except Exception as e:
            logger.error(f"Standalone analysis failed: {e}")
            raise e
