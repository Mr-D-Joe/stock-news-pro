"""Workflow orchestrator for full report generation pipeline."""

import os
import logging
import asyncio
from typing import Dict

from ai_service.models.article import ArticleCollection
from ai_service.config import Settings
from ai_service.processors.html_reporter import HtmlReporter
from ai_service.analyzers.provider_factory import ProviderFactory
from ai_service.models.contracts import PipelineResult, NewsItem, DeepWebSource

logger = logging.getLogger(__name__)


class WorkflowOrchestrator:
    """
    Orchestrates the entire report generation workflow:
    1. Resolve Ticker
    2. Collect Data (News, Prices, Fundamentals)
    3. Process Data (Identify Events)
    4. AI Analysis (Essay, SWOT)
    5. Generate Report (HTML)
    
    When DEV_MODE=true, uses mock providers for all data.
    """

    def __init__(self, settings: Settings):
        self.settings = settings
        self._is_dev_mode = settings.dev_mode
        
        if self._is_dev_mode:
            logger.info("=" * 60)
            logger.info("WorkflowOrchestrator running in DEV_MODE")
            logger.info("All data is MOCKED - NO external API calls")
            logger.info("=" * 60)

    def _get_ticker_resolver(self):
        """Get ticker resolver (mock or real based on DEV_MODE)."""
        if self._is_dev_mode:
            from ai_service.mock import get_mock_ticker_resolver
            return get_mock_ticker_resolver(self.settings)
        else:
            from ai_service.processors.ticker_resolver import TickerResolver
            return TickerResolver(self.settings)

    def _get_historic_analyzer(self):
        """Get historic analyzer (mock or real based on DEV_MODE)."""
        if self._is_dev_mode:
            from ai_service.mock import get_mock_historic_analyzer
            return get_mock_historic_analyzer(self.settings)
        else:
            from ai_service.fetchers.historic_analyzer import HistoricAnalyzer
            return HistoricAnalyzer(self.settings)

    def _get_deep_collector(self):
        """Get deep collector (mock or real based on DEV_MODE)."""
        if self._is_dev_mode:
            from ai_service.mock import get_mock_deep_collector
            return get_mock_deep_collector(self.settings)
        else:
            from ai_service.fetchers.deep_collector import DeepCollector
            return DeepCollector(self.settings)

    async def run(self, request: ArticleCollection, language: str) -> PipelineResult:
        """Execute the full report generation pipeline."""
        
        ticker = request.query_stocks[0] if request.query_stocks else "SPY"
        
        # 1. Resolve Company Name
        resolver = self._get_ticker_resolver()
        resolution = await resolver.resolve_stock(ticker)
        company_name = resolution["name"]
        ticker = resolution["symbol"] or ticker
        logger.info(f"Orchestrator starting for {company_name} ({ticker})")
        
        # 2. Fetch News (uses mock fetcher in DEV_MODE via get_fetcher)
        news_articles: list[NewsItem] = []
        news_items = []
        try:
            from ai_service.fetchers import get_fetcher
            fetcher = get_fetcher()
            news_items = await fetcher.fetch_for_ticker(ticker, max_items=50)
            logger.info(f"Fetched {len(news_items)} news items for report")
            
            # Convert to structured data for AI
            for n in news_items:
                news_articles.append({
                    "source": n.source,
                    "title": n.title,
                    "summary": n.summary,
                    "url": n.url,
                    "published": n.published
                })
        except Exception as e:
            logger.warning(f"News fetch failed, continuing with AI knowledge: {e}")

        # 2.5 Deep Web Search
        deep_collector = self._get_deep_collector()
        try:
            deep_items: list[DeepWebSource] = await deep_collector.collect(ticker, company_name, limit=6)
            logger.info(f"Deep Collector found {len(deep_items)} items")
            
            # In DEV_MODE, skip content fetching and summarization (data is pre-made)
            if not self._is_dev_mode:
                from ai_service.fetchers.content_fetcher import ContentFetcher
                content_fetcher = ContentFetcher(self.settings)
                summarizer = ProviderFactory.get_cheap_client(self.settings)
                
                summarized_count = 0
                for d in deep_items:
                    try:
                        full_text = await asyncio.to_thread(content_fetcher.fetch_url, d['url'])
                        
                        if full_text and len(full_text) > 1000 and summarized_count < 3:
                            smart_summary = await asyncio.to_thread(
                                summarizer.analyze_text, full_text[:10000], "summarize"
                            )
                            d['summary'] = f"[AI SUMMARY] {smart_summary}"
                            summarized_count += 1
                        elif full_text and len(full_text) > 200:
                            d['summary'] = full_text[:300] + "..."
                    except Exception as e:
                        logger.warning(f"Could not upgrade content for {d.get('url','')}: {e}")
            
            # Add deep items to news articles
            for d in deep_items:
                d['source'] = 'DeepWeb'
                news_articles.append(d)
                
                news_items.append(type('obj', (object,), {
                    'title': d['title'],
                    'published': d.get('published'),
                    'source': 'DeepWeb',
                    'url': d.get('url', ''),
                    'summary': d.get('summary', '')
                })())
                
        except Exception as e:
            logger.warning(f"Deep collection failed: {e}")
        
        # 3. Get Historical Price Data
        historic = self._get_historic_analyzer()
        periods = ["10y", "1y", "6mo", "3mo", "1mo", "1wk", "1d"]
        
        full_data = await historic.get_price_data(ticker, "10y")
        price_data = historic.slice_periods(full_data, periods)
        
        # 3.5 Get fundamentals
        fundamentals = request.fundamentals or {}
        if not fundamentals or "pe_ratio" not in fundamentals:
            logger.info(f"Fetching fundamentals for {ticker}...")
            try:
                fetched_funds = await historic.get_fundamentals(ticker)
                fundamentals = fetched_funds.copy()
                for key, val in (request.fundamentals or {}).items():
                    if val is not None and val != "N/A" and val != "":
                        fundamentals[key] = val
                        
                logger.info(f"Fundamentals fetch completed. Have P/E? {'pe_ratio' in fundamentals}")
            except Exception as e:
                logger.error(f"Fundamentals fetch failed: {e}")
    
        # 4. Get Pivotal Events
        events = await historic.identify_pivotal_events(ticker, company_name)
        
        # 5. Generate AI Analysis
        from ai_service.analyzers.essay_generator import EssayGenerator
        generator = EssayGenerator(self.settings)
        
        mainstream_news = [a for a in news_articles if a.get('source') != 'DeepWeb']
        deep_web_data = [a for a in news_articles if a.get('source') == 'DeepWeb']

        analysis_data = await asyncio.to_thread(
            generator.generate_analysis,
            ticker, company_name, language,
            news_context=mainstream_news,
            fundamentals=fundamentals,
            deep_sources=deep_web_data
        )
        
        # 5.5 Transform news into events
        news_as_events = []
        try:
            for n in news_items[:15]:
                pub_date = n.published
                if hasattr(pub_date, 'strftime'):
                    date_str = pub_date.strftime("%Y-%m-%d")
                else:
                    date_str = str(pub_date) if pub_date else ""
                    
                news_as_events.append({
                    "title": n.title,
                    "date": date_str,
                    "source": n.source,
                    "url": getattr(n, 'url', ''),
                    "summary": (n.summary or "")[:200] if n.summary else "",
                    "category": "News",
                    "impact": "medium"
                })
        except Exception as e:
            logger.warning(f"Failed to transform news to events: {e}")
        
        all_events = events + news_as_events
        
        if not fundamentals:
            fundamentals = {}
    
        sector = resolution.get("sector", fundamentals.get("sector", ""))
        business_context = fundamentals.get("business_summary", fundamentals.get("longBusinessSummary", ""))
        
        # 6. Generate HTML Report
        reporter = HtmlReporter()
        data = {
            "ticker": ticker,
            "company_name": company_name,
            "sector": sector,
            "business_context": business_context,
            "analysis": analysis_data,
            "price_data": price_data,
            "historic_events": all_events,
            "fundamentals": fundamentals,
            "last_price": price_data.get("1y", {}).get("last_price", "N/A"),
            "news_count": len(news_articles)
        }
        
        report_path = reporter.generate(data, language)
        
        return {
            "status": "success",
            "dev_mode": self._is_dev_mode,
            "report_path": os.path.abspath(report_path),
            "ticker": ticker,
            "company_name": company_name,
            "news_analyzed": len(news_articles),
            "items": all_events
        }
