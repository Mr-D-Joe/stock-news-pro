
import os
import logging
import asyncio
from typing import Dict, Any

from ai_service.models.article import ArticleCollection
from ai_service.config import Settings
from ai_service.processors.ticker_resolver import TickerResolver
from ai_service.fetchers.historic_analyzer import HistoricAnalyzer
from ai_service.processors.html_reporter import HtmlReporter
from ai_service.analyzers.provider_factory import ProviderFactory
import json
import re

logger = logging.getLogger(__name__)

class WorkflowOrchestrator:
    """
    Orchestrates the entire report generation workflow:
    1. Resolve Ticker
    2. Collect Data (News, Prices, Fundamentals)
    3. Process Data (Identify Events)
    4. AI Analysis (Essay, SWOT)
    5. Generate Report (HTML)
    """

    def __init__(self, settings: Settings):
        self.settings = settings

    async def run(self, request: ArticleCollection, language: str) -> Dict[str, Any]:
        """Execute the full report generation pipeline."""
        
        ticker = request.query_stocks[0] if request.query_stocks else "SPY"
        
        # 1. Resolve Company Name
        resolver = TickerResolver(self.settings)
        resolution = await resolver.resolve_stock(ticker)
        company_name = resolution["name"]
        ticker = resolution["symbol"] or ticker
        logger.info(f"Orchestrator starting for {company_name} ({ticker})")
        
        # 2. Fetch News (internal fetch if none provided)
        news_articles = []
        news_items = []  # Initialize for later use in events
        try:
            from ai_service.fetchers import get_fetcher
            fetcher = get_fetcher()
            news_items = await fetcher.fetch_for_ticker(ticker, max_items=50)
            logger.info(f"Fetched {len(news_items)} news items for report")
            
            # Convert to structured data for AI (keep as dicts, not strings)
            news_articles = []
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


        # 2.5 Deep Web Search (The "Investigator")
        try:
            from ai_service.fetchers.deep_collector import DeepCollector
            from ai_service.fetchers.content_fetcher import ContentFetcher
            from ai_service.analyzers.provider_factory import ProviderFactory
            
            deep_collector = DeepCollector(self.settings)
            content_fetcher = ContentFetcher(self.settings)
            
            # Initialize AI client for summarization (CHEAP model - preprocessing only)
            summarizer = ProviderFactory.get_cheap_client(self.settings)
            
            deep_items = await deep_collector.collect(ticker, company_name, limit=6)
            logger.info(f"Deep Collector found {len(deep_items)} items")
            
            # Add to news articles for AI context (limit AI summarization to TOP 3 to save API calls)
            summarized_count = 0
            for d in deep_items:
                # Upgrade: Fetch detailed content if possible (but limit AI calls)
                try:
                    logger.info(f"Deep Analysis: Fetching full content for {d['title']}...")

                    full_text = await asyncio.to_thread(content_fetcher.fetch_url, d['url'])
                    
                    # Only summarize TOP 3 items with sufficient content (save API calls)
                    if full_text and len(full_text) > 1000 and summarized_count < 3:
                        logger.info(f"Summarizing {len(full_text)} chars with AI...")
                        smart_summary = await asyncio.to_thread(summarizer.analyze_text, full_text[:10000], "summarize")
                        d['summary'] = f"[AI SUMMARY] {smart_summary}"
                        summarized_count += 1
                    elif full_text and len(full_text) > 200:
                        # Use first 300 chars as summary (no AI call)
                        d['summary'] = full_text[:300] + "..."
                        
                except Exception as e:
                    logger.warning(f"Could not upgrade content for {d['url']}: {e}")

                # Ensure deep items are compatible dicts
                d['source'] = 'DeepWeb' # Force source label just in case
                news_articles.append(d)
                
                # Also add to event list if relevant
                news_items.append(type('obj', (object,), {
                    'title': d['title'],
                    'published': d['published'],
                    'source': 'DeepWeb',
                    'url': d['url'],
                    'summary': d.get('summary', '')
                }))
        except Exception as e:
            logger.warning(f"Deep collection failed: {e}")
        
        # 3. Get Historical Price Data (Single API call, slice locally)
        historic = HistoricAnalyzer(self.settings)
        periods = ["10y", "1y", "6mo", "3mo", "1mo", "1wk", "1d"]
        
        # Fetch 10y data ONCE, then slice locally for other periods
        full_data = await historic.get_price_data(ticker, "10y")
        price_data = historic.slice_periods(full_data, periods)
        
        # 3.5 Get fundamentals (Fetch if missing - Intensive Data Collection)
        fundamentals = request.fundamentals or {}
        if not fundamentals or "pe_ratio" not in fundamentals or "target_mean_price" not in fundamentals:
            logger.info(f"Fundamentals missing/incomplete for {ticker}. Starting intensive data fetch...")
            try:
                fetched_funds = await historic.get_fundamentals(ticker)
                
                # Smart Merge: Only overwrite cached/fetched data if request has valid (non-None) new data
                fundamentals = fetched_funds.copy()
                for key, val in (request.fundamentals or {}).items():
                    if val is not None and val != "N/A" and val != "":
                        fundamentals[key] = val
                
                logger.info(f"Intensive fetch completed. Have P/E? {'pe_ratio' in fundamentals}")
            except Exception as e:
                logger.error(f"Intensive data fetch failed: {e}")
    
        # 4. Get Pivotal Events (AI-identified)
        events = await historic.identify_pivotal_events(ticker, company_name)
        
        # 5. Generate AI Analysis with news context
        from ai_service.analyzers.essay_generator import EssayGenerator
        generator = EssayGenerator(self.settings)
        
        # Split news and deep web data
        # 'news_articles' currently contains both appended. Ideally, we should have kept them valid.
        # But since I appended deep data to news_articles in lines 60-70ish, I can either separate them here 
        # based on 'source' == 'DeepWeb' or just pass the full list to both if I handled it carefully.
        # However, to use the new "Dual Input" logic best:
        
        mainstream_news = [a for a in news_articles if a.get('source') != 'DeepWeb']
        deep_web_data = [a for a in news_articles if a.get('source') == 'DeepWeb']

        analysis_data = await asyncio.to_thread(
            generator.generate_analysis,
            ticker, company_name, language,
            news_context=mainstream_news,
            fundamentals=fundamentals,
            deep_sources=deep_web_data
        )
        
        # 5.5 Also transform fetched news into historic_events format for the table
        news_as_events = []
        try:
            for n in news_items[:15]:  # Top 15 news items
                news_as_events.append({
                    "title": n.title,
                    "date": n.published.strftime("%Y-%m-%d") if n.published else "",
                    "source": n.source,
                    "url": n.url,
                    "summary": n.summary[:200] if n.summary else "",
                    "category": "News",
                    "impact": "medium"
                })
        except Exception as e:
            logger.warning(f"Failed to transform news to events: {e}")
        
        # Merge AI events + news events
        all_events = events + news_as_events
        
        # Check fundamentals finally
        if not fundamentals:
             fundamentals = {}
    
        sector = resolution.get("sector", fundamentals.get("sector", ""))
        business_context = fundamentals.get("business_summary", fundamentals.get("longBusinessSummary", ""))
        
        # 6. Generate HTML
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
            "report_path": os.path.abspath(report_path),
            "ticker": ticker,
            "company_name": company_name,
            "news_analyzed": len(news_articles),
            "items": all_events  # Return events/news for GUI "News Tracker"
        }


