"""Impact analyzer for correlating news with stock price movements."""

from __future__ import annotations

import logging
import re
from typing import Optional, TYPE_CHECKING


from ai_service.analyzers.base_client import BaseAIClient, AIError
from ai_service.analyzers.provider_factory import ProviderFactory
from ai_service.analyzers.prompts import build_impact_relevance_prompt, SYSTEM_INSTRUCTION_ANALYST
from ai_service.config import Settings
from ai_service.models.article import Article
from ai_service.models.impact import ArticleImpact, ImpactAnalysisResult, NewsCategory, StockSensitivity
from ai_service.models.price_data import PriceHistory

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from ai_service.pipeline.base import PipelineContext

# Impact weights by category (1.0 = baseline, higher = more impact)
CATEGORY_WEIGHTS: dict[NewsCategory, float] = {
    NewsCategory.FDA_APPROVAL: 5.0,
    NewsCategory.FDA_REJECTION: 5.0,
    NewsCategory.EARNINGS: 4.0,
    NewsCategory.PARTNERSHIP: 4.0,
    NewsCategory.ACQUISITION: 4.5,
    NewsCategory.ANALYST_RATING: 3.0,
    NewsCategory.PRODUCT_LAUNCH: 3.5,
    NewsCategory.CLINICAL_TRIAL: 4.0,
    NewsCategory.REGULATORY: 3.5,
    NewsCategory.EXECUTIVE: 2.5,
    NewsCategory.GENERAL_NEWS: 2.0,
    NewsCategory.RUMOR: 1.5,
}


# Keywords for category detection
CATEGORY_KEYWORDS: dict[NewsCategory, list[str]] = {
    NewsCategory.FDA_APPROVAL: [
        "fda approves", "fda approval", "fda clears", "fda grants",
        "regulatory approval", "approval granted", "fda accepted"
    ],
    NewsCategory.FDA_REJECTION: [
        "fda rejects", "fda rejection", "crl", "complete response letter",
        "fda denies", "approval denied", "fda declines"
    ],
    NewsCategory.EARNINGS: [
        "earnings", "quarterly results", "revenue", "eps", "profit",
        "q1", "q2", "q3", "q4", "annual report", "financial results"
    ],
    NewsCategory.PARTNERSHIP: [
        "partnership", "collaboration", "joint venture", "alliance",
        "strategic agreement", "licensing deal", "partner"
    ],
    NewsCategory.ACQUISITION: [
        "acquisition", "acquire", "merger", "buyout", "takeover",
        "purchase agreement", "acquired by", "to buy"
    ],
    NewsCategory.ANALYST_RATING: [
        "upgrade", "downgrade", "price target", "analyst", "rating",
        "buy rating", "sell rating", "hold rating", "outperform"
    ],
    NewsCategory.PRODUCT_LAUNCH: [
        "launch", "launches", "introducing", "new product", "release",
        "available now", "commercial launch"
    ],
    NewsCategory.CLINICAL_TRIAL: [
        "clinical trial", "phase 1", "phase 2", "phase 3", "trial results",
        "study results", "efficacy", "safety data", "pivotal trial"
    ],
    NewsCategory.REGULATORY: [
        "regulatory", "sec", "compliance", "investigation", "lawsuit",
        "legal", "settlement"
    ],
    NewsCategory.EXECUTIVE: [
        "ceo", "cfo", "cto", "executive", "appoints", "resignation",
        "management change", "leadership"
    ],
    NewsCategory.RUMOR: [
        "rumor", "speculation", "reportedly", "sources say", "unconfirmed",
        "may be", "could be", "might"
    ],
}



class ImpactAnalyzer:
    """Analyzes news articles for potential stock price impact."""
    
    def __init__(self, settings: Optional[Settings] = None, language: str = "German"):
        self.settings = settings or Settings()
        self.language = language
        self.category_weights = CATEGORY_WEIGHTS
        self.category_keywords = CATEGORY_KEYWORDS
        # Pre-compile regex for faster matching
        self._compiled_keywords = {
            cat: [re.compile(rf"\b{re.escape(kw)}\b", re.IGNORECASE) for kw in kws]
            for cat, kws in self.category_keywords.items()
        }
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
    
    def categorize_article(self, article: Article) -> NewsCategory:
        """
        Determine the category of an article based on content.
        
        Args:
            article: Article to categorize
            
        Returns:
            Most likely NewsCategory
        """
        text_to_search = f"{article.title} {article.text or ''}".lower()
        
        # Check each category's keywords
        category_scores: dict[NewsCategory, int] = {}
        
        for category, patterns in self._compiled_keywords.items():
            score = 0
            for pattern in patterns:
                if pattern.search(text_to_search):
                    score += 1
            if score > 0:
                category_scores[category] = score
        
        if not category_scores:
            # Check source for rumor indicators
            if article.article_type == "discussion":
                return NewsCategory.RUMOR
            return NewsCategory.GENERAL_NEWS
        
        # Return category with highest keyword matches
        return max(category_scores, key=lambda k: category_scores[k])
    
    def analyze_article(
        self, 
        article: Article, 
        price_history: Optional[PriceHistory] = None
    ) -> ArticleImpact:
        """
        Analyze a single article for impact.
        
        Args:
            article: Article to analyze
            price_history: Optional price history for correlation
            
        Returns:
            ArticleImpact with scores and category
        """
        category = self.categorize_article(article)
        base_weight = self.category_weights.get(category, 2.0)
        
        impact = ArticleImpact(
            article_title=article.title,
            article_link=article.link,
            published=article.published,
            category=category,
            base_weight=base_weight
        )
        
        # Try to correlate with price movement if we have data
        if price_history and article.published:
            price_change = price_history.get_price_change_around_date(
                article.published,
                days_before=1,
                days_after=3
            )
            impact.price_before = price_change.get("before")
            impact.price_after = price_change.get("after")
            impact.price_change_pct = price_change.get("change_pct")
        
        return impact
    
    def determine_stock_sensitivity(
        self, 
        price_history: PriceHistory
    ) -> StockSensitivity:
        """
        Analyze price history to identify what drives this specific stock.
        
        Args:
            price_history: Historical price data
            
        Returns:
            StockSensitivity profile
        """
        symbol = price_history.symbol
        prices = price_history.prices
        
        if not prices:
            return StockSensitivity(symbol=symbol)
            
        # Calculate average daily move
        moves = [abs(p.daily_change_pct) for p in prices]
        avg_move = sum(moves) / len(moves) if moves else 0.0
        
        # Identify high volatility events (e.g., top 1% of moves)
        threshold = avg_move * 3  # Simplified threshold
        high_vol_events = [p.date for p in prices if abs(p.daily_change_pct) >= threshold]
        
        # Determine sensitivity score relative to a "typical" stock (e.g., 2% avg move)
        sensitivity_score = round(avg_move / 2.0, 2)
        
        profile = StockSensitivity(
            symbol=symbol,
            avg_daily_move_pct=round(avg_move, 2),
            volatility_high_events=high_vol_events[:20],  # Limit to top recent ones
            sensitivity_score=max(0.5, sensitivity_score)
        )
        
        return profile

    def analyze_articles(
        self, 
        articles: list[Article], 
        price_history: Optional[PriceHistory] = None,
        symbol: str = "UNKNOWN"
    ) -> ImpactAnalysisResult:
        """
        Analyze multiple articles for impact.
        
        Args:
            articles: List of articles to analyze
            price_history: Optional price history for correlation
            symbol: Stock symbol being analyzed
            
        Returns:
            Complete ImpactAnalysisResult
        """
        logger.info(f"Analyzing {len(articles)} articles for impact on {symbol}")
        
        impacts = []
        category_counts: dict[str, int] = {}
        
        for article in articles:
            impact = self.analyze_article(article, price_history)
            impacts.append(impact)
            
            # Track category counts
            cat_name = impact.category.value
            category_counts[cat_name] = category_counts.get(cat_name, 0) + 1
        
        # Calculate summary stats
        avg_score = 0.0
        high_impact = 0
        
        if impacts:
            avg_score = sum(i.impact_score for i in impacts) / len(impacts)
            high_impact = sum(1 for i in impacts if i.impact_score >= 5.0)
        
        result = ImpactAnalysisResult(
            symbol=symbol,
            articles_analyzed=len(articles),
            article_impacts=impacts,
            avg_impact_score=round(avg_score, 2),
            high_impact_count=high_impact,
            category_breakdown=category_counts
        )
        
        # Add sensitivity profile if we have price history
        if price_history:
            result.sensitivity_profile = self.determine_stock_sensitivity(price_history)
            
        return result

    def enrich_with_ai(self, result: ImpactAnalysisResult, articles: list[Article]) -> None:
        """Enrich high-impact articles with AI-driven relevance and explanations."""
        # Focus on articles with impact_score >= 5 or top events
        target_impacts = [i for i in result.article_impacts if i.impact_score >= 5.0]
        if not target_impacts:
            return

        # Prepare articles for AI analysis (titles and summaries)
        ai_input = []
        # Mapping to correlate AI results back to ArticleImpact objects
        impact_map = {}
        
        for i, impact in enumerate(target_impacts):
            article = next((a for a in articles if a.link == impact.article_link), None)
            if article:
                ai_input.append({
                    "title": article.title,
                    "summary": article.summary or article.title[:500]
                })
                impact_map[len(ai_input) - 1] = impact

        if not ai_input:
            return

        logger.info(f"Enriching {len(ai_input)} impacts with AI for {result.symbol}")
        
        prompt = build_impact_relevance_prompt(
            articles=ai_input,
            stock_symbol=result.symbol,
            language=self.language
        )
        
        # Ensure client has UI callbacks from current context (if available)
        # However, enrich_with_ai doesn't take context. 
        # For now, we assume the client was already initialized or we'd need to pass it.
        
        try:
            response = self.client.generate(
                prompt=prompt,
                system_instruction=SYSTEM_INSTRUCTION_ANALYST,
                temperature=0.2, # Low temperature for consistent JSON
            )
            
            # Extract JSON from response (Gemini sometimes wraps in markdown)
            json_str = response.strip()
            if json_str.startswith("```json"):
                json_str = json_str.split("```json", 1)[1].split("```", 1)[0].strip()
            elif json_str.startswith("```"):
                json_str = json_str.split("```", 1)[1].split("```", 1)[0].strip()
                
            import json
            analysis_data = json.loads(json_str)
            
            for item in analysis_data:
                idx = item.get("id")
                if idx in impact_map:
                    impact = impact_map[idx]
                    impact.relevance_score = item.get("relevance_score", 1.0)
                    impact.relevance_explanation = item.get("explanation")
                    
                    # Update base weight if highly relevant
                    if impact.relevance_score > 0.8:
                        impact.base_weight *= (1.0 + (impact.relevance_score - 0.5))
                    elif impact.relevance_score < 0.3:
                         impact.base_weight *= 0.5
                         
            logger.info(f"AI enrichment complete for {result.symbol}")
            
        except (AIError, Exception) as e:
            logger.warning(f"AI impact enrichment failed: {e}")
