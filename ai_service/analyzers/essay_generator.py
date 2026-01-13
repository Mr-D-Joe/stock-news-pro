"""Essay generator with AI-powered analysis."""

from __future__ import annotations

import logging
import re
from typing import Optional

from stock_news_ai.analyzers.base_client import BaseAIClient, AIError
from stock_news_ai.analyzers.provider_factory import ProviderFactory
from stock_news_ai.analyzers.prompts import (
    SYSTEM_INSTRUCTION_ANALYST,
    build_anomaly_detection_prompt,
    build_essay_prompt,
)
from stock_news_ai.config import Settings
from stock_news_ai.models.article import AnalysisResult, ArticleCollection, CalendarEvent
from stock_news_ai.pipeline.base import PipelineContext, PipelineStep

logger = logging.getLogger(__name__)


class EssayGenerator(PipelineStep[ArticleCollection, AnalysisResult]):
    """Generate analytical essays from article collections using AI."""

    name = "essay_generator"

    def __init__(
        self,
        settings: Optional[Settings] = None,
        language: str = "German",
        include_anomaly_analysis: bool = False,  # Disabled by default for free tier
        max_articles_for_ai: int = 20,  # Limit articles to reduce token usage
    ):
        self.settings = settings or Settings()
        self.language = language
        self.include_anomaly_analysis = include_anomaly_analysis
        self.max_articles_for_ai = max_articles_for_ai
        self._client: Optional[BaseAIClient] = None

    @property
    def client(self) -> BaseAIClient:
        """Lazy-initialize AI client."""
        if self._client is None:
            self._client = ProviderFactory.get_client("gemini", self.settings)
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
        """Generate essay from article collection."""
        self._ensure_client_callbacks(context)
        if input_data.count == 0:
            logger.warning("No articles to analyze")
            return AnalysisResult(
                essay="No articles were collected for analysis.",
                summary="No data available.",
                article_collection=input_data,
            )

        # Get focus parameters and language from context
        stocks = input_data.query_stocks or context.config.stocks
        sectors = input_data.query_sectors or context.config.sectors
        language = context.config.language if hasattr(context.config, 'language') else self.language

        logger.info(f"Generating essay for {input_data.count} articles")
        
        # Limit articles for AI to reduce token usage and API calls
        articles_for_ai = input_data
        if input_data.count > self.max_articles_for_ai:
            logger.info(f"Limiting to top {self.max_articles_for_ai} articles for AI analysis")
            limited_articles = input_data.articles[:self.max_articles_for_ai]
            articles_for_ai = ArticleCollection(
                articles=limited_articles,
                query_stocks=input_data.query_stocks,
                query_sectors=input_data.query_sectors,
                collected_at=input_data.collected_at,
            )
            articles_for_ai.assign_citation_ids()
        
        # Generate main essay
        essay_prompt = build_essay_prompt(
            articles=articles_for_ai,
            focus_stocks=stocks,
            focus_sectors=sectors,
            language=self.language,
            sensitivity_profile=input_data.impact_analysis.sensitivity_profile if input_data.impact_analysis else None,
            fundamentals=input_data.fundamentals,
        )
        
        try:
            essay = self.client.generate(
                prompt=essay_prompt,
                system_instruction=SYSTEM_INSTRUCTION_ANALYST,
                temperature=0.7,
            )
        except AIError as e:
            logger.error(f"Essay generation failed: {e}")
            essay = f"Essay generation failed: {e}"

        # Initialize result
        result = AnalysisResult(
            essay=essay,
            article_collection=input_data,
            impact_analysis=input_data.impact_analysis,
            price_history=input_data.price_history,
            fundamentals=input_data.fundamentals,
        )

        # Extract key findings and summary from the essay
        result.summary = self._extract_summary(essay)
        result.key_findings = self._extract_key_findings(essay)
        result.swot = self._extract_swot(essay)
        result.watch_items = self._extract_watch_items(essay)
        result.upcoming_events = self._extract_upcoming_events(essay)

        # Optionally run anomaly detection
        if self.include_anomaly_analysis and input_data.count >= 5:
            anomalies = self._detect_anomalies(input_data)
            result.anomalies = anomalies

        # Determine overall sentiment
        result.sentiment = self._analyze_sentiment(essay)

        logger.info(f"Generated essay: {len(essay)} chars, {len(result.key_findings)} findings")
        return result

    def _extract_summary(self, essay: str) -> str:
        """Extract executive summary from essay."""
        # Look for summary section
        lower = essay.lower()
        if "executive summary" in lower:
            start = lower.find("executive summary")
            # Find the next section header or take first paragraph
            lines = essay[start:].split("\n")
            summary_lines = []
            for line in lines[1:]:  # Skip the header
                if line.strip().startswith("#") or line.strip().startswith("##"):
                    break
                if line.strip():
                    summary_lines.append(line.strip())
                if len(summary_lines) >= 3:
                    break
            if summary_lines:
                return " ".join(summary_lines)
        
        # Fallback: first paragraph
        paragraphs = essay.split("\n\n")
        for p in paragraphs:
            if len(p.strip()) > 50 and not p.startswith("#"):
                return p.strip()[:500]
        
        return essay[:300] if essay else ""

    def _extract_key_findings(self, essay: str) -> list[str]:
        """Extract key findings bullet points from essay."""
        findings = []
        lines = essay.split("\n")
        in_findings = False
        
        for line in lines:
            lower = line.lower()
            if "key finding" in lower or "key insight" in lower or "key takeaway" in lower:
                in_findings = True
                continue
            
            if in_findings:
                # Stop at next major section
                if line.startswith("##") or line.startswith("# "):
                    break
                # Capture bullet points
                stripped = line.strip()
                match = re.match(r'^[-*•→\d.]+\s+(.+)$', stripped)
                if match:
                    finding = match.group(1).strip()
                    if finding and len(finding) > 10:
                        findings.append(finding)
        
        return findings[:10]  # Limit to 10 findings

    def _extract_swot(self, essay: str) -> dict[str, list[str]]:
        """Extract SWOT analysis categories and items from the essay."""
        swot = {"Strengths": [], "Weaknesses": [], "Opportunities": [], "Threats": []}
        lines = essay.split("\n")
        current_category = None
        
        # Keywords to identify SWOT sections (German and English)
        cat_map = {
            "strength": "Strengths", "stärken": "Strengths",
            "weakness": "Weaknesses", "schwächen": "Weaknesses",
            "opportunity": "Opportunities", "chancen": "Opportunities",
            "threat": "Threats", "risiken": "Threats", "gefahren": "Threats"
        }
        
        in_swot_section = False
        for line in lines:
            lower = line.lower()
            
            # Detect SWOT section or a specific category header
            if "swot" in lower:
                in_swot_section = True
                continue
                
            # Check for category change
            found_header = False
            for kw, cat in cat_map.items():
                if kw in lower and (line.startswith("###") or line.startswith("**") or line.endswith(":")):
                    current_category = cat
                    found_header = True
                    break
            
            if found_header:
                continue
                
            if current_category:
                # Capture bullet points if we have a category
                if line.startswith("##") or (line.startswith("# ") and not in_swot_section):
                    current_category = None
                    continue
                    
                stripped = line.strip()
                match = re.match(r'^[-*•→\d.]+\s+(.+)$', stripped)
                if match:
                    item = match.group(1).strip()
                    if item and len(item) > 10:
                        swot[current_category].append(item)
                    
        # Filter out empty categories
        return {k: v for k, v in swot.items() if v}

    def _extract_watch_items(self, essay: str) -> list[str]:
        """Extract critical watch items from essay."""
        items = []
        lines = essay.split("\n")
        in_watch = False
        
        watch_keywords = ["watch item", "beobachtung", "beachtet", "focus", "achtung", "kritisch"]
        
        for line in lines:
            lower = line.lower()
            if any(kw in lower for kw in watch_keywords) and (line.startswith("##") or "**" in line):
                in_watch = True
                continue
            
            if in_watch:
                if line.startswith("##") or line.startswith("# "):
                    break
                stripped = line.strip()
                match = re.match(r'^[-*•→\d.]+\s+(.+)$', stripped)
                if match:
                    item = match.group(1).strip()
                    if item and len(item) > 10:
                        items.append(item)
                        
        return items[:5]

    def _extract_upcoming_events(self, essay: str) -> list[CalendarEvent]:
        """Extract upcoming calendar events from essay."""
        events = []
        lines = essay.split("\n")
        in_events = False
        
        event_keywords = ["calender", "kalender", "termin", "date", "event", "upcoming", "bevorstehend"]
        
        for line in lines:
            lower = line.lower()
            if any(kw in lower for kw in event_keywords) and (line.startswith("##") or "**" in line):
                in_events = True
                continue
            
            if in_events:
                if line.startswith("##") or line.startswith("# "):
                    break
                stripped = line.strip()
                # Look for patterns like: "2024-05-15: Q1 Earnings Call" or "- 15. Mai: HV"
                match = re.match(r'^[-*•→\d.]+\s+([^:]+):\s+(.+)$', stripped)
                if match:
                    date_part = match.group(1).strip()
                    title_part = match.group(2).strip()
                    events.append(CalendarEvent(
                        title=title_part,
                        date=date_part,
                        description=f"Automated extraction: {title_part}"
                    ))
                else:
                    # Fallback for simple bullet points without colon
                    match = re.match(r'^[-*•→\d.]+\s+(.+)$', stripped)
                    if match:
                        text = match.group(1).strip()
                        if any(char.isdigit() for char in text) and len(text) > 5:
                            events.append(CalendarEvent(
                                title=text,
                                date="Check news for date",
                                description=text
                            ))
                        
        return events[:5]

    def _detect_anomalies(self, articles: ArticleCollection) -> list[str]:
        """Run anomaly detection on article collection."""
        prompt = build_anomaly_detection_prompt(articles)
        
        try:
            response = self.client.generate(
                prompt=prompt,
                temperature=0.3,
                max_output_tokens=1024,
            )
            
            # Extract bullet points from response
            anomalies = []
            for line in response.split("\n"):
                stripped = line.strip()
                match = re.match(r'^[-*•→]+\s+(.+)$', stripped)
                if match:
                    anomaly = match.group(1).strip()
                    if anomaly and len(anomaly) > 15:
                        anomalies.append(anomaly)
            
            return anomalies[:5]  # Top 5 anomalies
            
        except AIError as e:
            logger.warning(f"Anomaly detection failed: {e}")
            return []

    def _analyze_sentiment(self, essay: str) -> str:
        """Determine overall sentiment from essay content."""
        lower = essay.lower()
        
        positive_words = ["positive", "growth", "increase", "profit", "success", "optimistic", "strong"]
        negative_words = ["negative", "decline", "decrease", "loss", "concern", "risk", "weak"]
        
        positive_count = sum(1 for word in positive_words if word in lower)
        negative_count = sum(1 for word in negative_words if word in lower)
        
        if positive_count > negative_count + 2:
            return "positive"
        elif negative_count > positive_count + 2:
            return "negative"
        else:
            return "neutral"
