
import logging
import asyncio
from typing import List, Dict, Any
from datetime import datetime
from duckduckgo_search import DDGS
from ai_service.config import Settings

logger = logging.getLogger(__name__)

class DeepCollector:
    """
    "Deep Web" collector that actively hunts for information using search engines.
    Goes beyond passive RSS feeds to find analysis, PDFs, and forum discussions.
    """

    def __init__(self, settings: Settings = None):
        self.settings = settings or Settings()
        # Rate limiting or concurrency control could go here

    async def collect(self, ticker: str, company_name: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Perform a deep dive search for the given ticker.
        """
        logger.info(f"Starting Deep Web collection for {ticker} ({company_name})...")
        
        results = []
        
        # Define simple keyword-based search strategies (DDG doesn't support complex site: operators)
        queries = [
            f"{ticker} stock analysis outlook",
            f"{company_name} investment thesis 2025",
            f"{ticker} earnings analysis forecast",
            f"{ticker} analyst rating buy sell"
        ]
        
        # Run searches (could be parallelized, but DDG might rate limit)
        for q in queries:
            try:
                # Run in executor to avoid blocking if DDGS is sync 
                items = await asyncio.to_thread(self._search_ddg, q, 3)
                results.extend(items)
            except Exception as e:
                logger.warning(f"Deep search query '{q}' failed: {e}")

        # Deduplicate by URL - minimal filtering to ensure we get results
        # Only filter truly irrelevant help/support pages
        irrelevant_patterns = ['support.google.com', '/help/', 'mail.yahoo.com']
        unique_results = {}
        filtered_count = 0
        for r in results:
            url = r.get('href', '')
            if not url:
                continue
            # Only skip obvious help pages
            if any(pattern in url.lower() for pattern in irrelevant_patterns):
                filtered_count += 1
                continue
            if url not in unique_results:
                unique_results[url] = r
        
        final_list = list(unique_results.values())
        logger.info(f"Deep Collector found {len(final_list)} sources (filtered {filtered_count} irrelevant)")
        
        # Transform to standard "Article/Source" format
        formatted = []
        for r in final_list[:limit * 2]: # Return a bit more, filtering happens later
            formatted.append({
                "title": r.get('title', 'Unknown Title'),
                "url": r.get('href', ''),
                "summary": r.get('body', ''),
                "source": "DeepWeb",
                "published": datetime.now(), # DDG doesn't always give date, assume fresh
                "is_deep_source": True
            })
            
        return formatted

    def _search_ddg(self, query: str, max_results: int) -> List[Dict]:
        """Synchronous wrapper for DDGS."""
        try:
            with DDGS() as ddgs:
                # Default backend is usually best now
                return list(ddgs.text(query, max_results=max_results))
        except Exception as e:
             logger.warning(f"DDGS Text search failed: {e}")
             return []

if __name__ == "__main__":
    # Test runner
    async def main():
        c = DeepCollector()
        res = await c.collect("ABSI", "Absci Corporation")
        import json
        print(json.dumps(res, indent=2, default=str))

    asyncio.run(main())
