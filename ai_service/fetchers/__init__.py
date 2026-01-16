"""News fetching service for multiple sources.

Supports:
- RSS Feeds (Google Finance, Yahoo Finance, etc.)
- Stock-specific news via yfinance
- Free News APIs
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Optional
from dataclasses import dataclass

import feedparser
import yfinance as yf
from bs4 import BeautifulSoup
import requests

logger = logging.getLogger(__name__)


@dataclass
class FetchedNews:
    """Represents a fetched news item."""
    ticker: str
    title: str
    source: str
    url: Optional[str] = None
    published: Optional[datetime] = None
    summary: Optional[str] = None


class NewsFetcher:
    """Multi-source news fetcher with 15+ sources."""
    
    # Comprehensive RSS Feed templates for stock news
    RSS_FEEDS = {
        # Major Financial News - Stock-specific
        "google_finance": "https://news.google.com/rss/search?q={ticker}+stock&hl=en-US&gl=US&ceid=US:en",
        "google_company": "https://news.google.com/rss/search?q={company_name}&hl=en-US&gl=US&ceid=US:en",
        "yahoo_finance": "https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US",
        
        # Financial Analyst Sites
        "seeking_alpha": "https://seekingalpha.com/api/sa/combined/{ticker}.xml",
        "benzinga": "https://www.benzinga.com/stock/{ticker}/feed",
        "marketwatch": "https://feeds.marketwatch.com/marketwatch/topstories/",
        "cnbc": "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114",
        
        # General Business News (filtered later)
        "reuters_business": "https://feeds.reuters.com/reuters/businessNews",
        "bloomberg_markets": "https://feeds.bloomberg.com/markets/news.rss",
        "wsj_markets": "https://feeds.a]wsj.com/rss/RSSMarketsMain.xml",
        
        # Tech-focused (good for tech stocks)
        "techcrunch": "https://techcrunch.com/feed/",
        "theverge": "https://www.theverge.com/rss/index.xml",
        
        # German/EU Sources
        "finanzen_net": "https://www.finanzen.net/rss/news",
        "handelsblatt": "https://www.handelsblatt.com/contentexport/feed/finanzen",
        "boerse_de": "https://www.boerse.de/rss/nachrichten",
    }
    
    # Company name mappings for better search
    COMPANY_NAMES = {
        "AAPL": "Apple",
        "GOOGL": "Google Alphabet",
        "MSFT": "Microsoft",
        "AMZN": "Amazon",
        "META": "Meta Facebook",
        "TSLA": "Tesla",
        "NVDA": "NVIDIA",
        "MBG.DE": "Mercedes-Benz",
        "BMW.DE": "BMW",
        "VOW3.DE": "Volkswagen",
        "LLY": "Eli Lilly",
        "ABSI": "Absci",
    }
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (compatible; StockNewsPro/2.0; +https://stocknewspro.app)"
        })
    
    async def fetch_for_ticker(self, ticker: str, max_items: int = 30) -> list[FetchedNews]:
        """
        Fetch news from 10+ sources for a ticker.
        
        Sources (in order):
        1. Google Finance RSS (ticker-based)
        2. Google News (company name-based)
        3. Yahoo Finance RSS
        4. Seeking Alpha
        5. Benzinga
        6. yfinance library
        7. Reddit communities
        8. General financial RSS feeds (filtered)
        """
        all_news = []
        company_name = self.COMPANY_NAMES.get(ticker.upper(), ticker)
        
        # 1. Google Finance RSS (usually best results)
        google_news = await self._fetch_rss(ticker, "google_finance", max_items)
        all_news.extend(google_news)
        logger.info(f"Google Finance: {len(google_news)} items for {ticker}")
        
        # 2. Google News with company name
        google_company = await self._fetch_rss_with_company(company_name, "google_company", max_items // 2)
        all_news.extend(google_company)
        logger.info(f"Google Company: {len(google_company)} items for {company_name}")
        
        # 3. Yahoo Finance RSS
        yahoo_news = await self._fetch_rss(ticker, "yahoo_finance", max_items // 2)
        all_news.extend(yahoo_news)
        logger.info(f"Yahoo RSS: {len(yahoo_news)} items for {ticker}")
        
        # 4. Seeking Alpha
        sa_news = await self._fetch_rss(ticker, "seeking_alpha", max_items // 3)
        all_news.extend(sa_news)
        logger.info(f"Seeking Alpha: {len(sa_news)} items for {ticker}")
        
        # 5. Benzinga
        bz_news = await self._fetch_rss(ticker, "benzinga", max_items // 3)
        all_news.extend(bz_news)
        logger.info(f"Benzinga: {len(bz_news)} items for {ticker}")
        
        # 6. yfinance library
        yf_news = await self._fetch_yfinance(ticker, max_items // 2)
        all_news.extend(yf_news)
        logger.info(f"yfinance: {len(yf_news)} items for {ticker}")
        
        # 7. Reddit (community posts/rumors)
        try:
            from ai_service.fetchers.reddit_fetcher import get_reddit_fetcher
            reddit_fetcher = get_reddit_fetcher()
            reddit_posts = await reddit_fetcher.fetch_for_ticker(ticker, max_items // 3)
            for post in reddit_posts:
                all_news.append(FetchedNews(
                    ticker=post.ticker,
                    title=f"[Reddit] {post.title}",
                    source=f"r/{post.subreddit}",
                    url=post.url,
                    published=post.published,
                    summary=post.selftext
                ))
            logger.info(f"Reddit: {len(reddit_posts)} posts for {ticker}")
        except Exception as e:
            logger.warning(f"Reddit integration failed: {e}")
        
        # 8. General financial RSS (filtered by ticker/company name)
        for feed_name in ["marketwatch", "reuters_business", "cnbc"]:
            try:
                general_news = await self._fetch_general_rss(ticker, company_name, feed_name, 5)
                all_news.extend(general_news)
            except:
                pass
        
        # Remove duplicates based on title
        seen_titles = set()
        unique_news = []
        for item in all_news:
            title_key = item.title.lower()[:50]
            if title_key not in seen_titles:
                seen_titles.add(title_key)
                unique_news.append(item)
        
        logger.info(f"TOTAL unique news for {ticker}: {len(unique_news)} items from multiple sources")
        return unique_news
    
    async def _fetch_rss_with_company(self, company_name: str, feed_name: str, max_items: int) -> list[FetchedNews]:
        """Fetch RSS with company name instead of ticker."""
        if feed_name not in self.RSS_FEEDS:
            return []
        
        import urllib.parse
        encoded_name = urllib.parse.quote(company_name)
        url = self.RSS_FEEDS[feed_name].replace("{company_name}", encoded_name)
        
        return await self._fetch_rss_url(url, feed_name, company_name, max_items)
    
    async def _fetch_general_rss(self, ticker: str, company_name: str, feed_name: str, max_items: int) -> list[FetchedNews]:
        """Fetch general RSS and filter for relevant articles."""
        if feed_name not in self.RSS_FEEDS:
            return []
        
        url = self.RSS_FEEDS[feed_name]
        all_items = await self._fetch_rss_url(url, feed_name, ticker, max_items * 3)
        
        # Filter to only relevant articles
        keywords = [ticker.lower(), company_name.lower()]
        relevant = [
            item for item in all_items 
            if any(kw in item.title.lower() or (item.summary and kw in item.summary.lower()) for kw in keywords)
        ]
        
        return relevant[:max_items]
    
    async def _fetch_yfinance(self, ticker: str, max_items: int) -> list[FetchedNews]:
        """Fetch news via yfinance library."""
        news_items = []
        
        try:
            loop = asyncio.get_event_loop()
            
            # yfinance calls can be blocking
            def fetch_yf_news():
                t = yf.Ticker(ticker)
                return t.news
            
            news = await loop.run_in_executor(None, fetch_yf_news)
            
            if not news:
                return []
            
            for item in news[:max_items]:
                published = None
                if "providerPublishTime" in item:
                    published = datetime.fromtimestamp(item["providerPublishTime"])
                
                news_items.append(FetchedNews(
                    ticker=ticker,
                    title=item.get("title", "No title"),
                    source=item.get("publisher", "Unknown"),
                    url=item.get("link", ""),
                    published=published,
                    summary=item.get("summary", "")[:300] if item.get("summary") else None
                ))
                
        except Exception as e:
            logger.warning(f"yfinance fetch failed for {ticker}: {e}")
        
        return news_items
    
    async def _fetch_rss(self, ticker: str, feed_name: str, max_items: int) -> list[FetchedNews]:
        """Fetch news from RSS feed."""
        news_items = []
        
        if feed_name not in self.RSS_FEEDS:
            return []
        
        url = self.RSS_FEEDS[feed_name].format(ticker=ticker)
        
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            feed = feedparser.parse(response.text)
            
            for entry in feed.entries[:max_items]:
                # Parse published date
                published = None
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    try:
                        published = datetime(*entry.published_parsed[:6])
                    except:
                        pass
                
                # Clean title
                title = entry.get("title", "No title")
                if hasattr(title, "replace"):
                    title = BeautifulSoup(title, "html.parser").get_text()
                
                # Get summary
                summary = entry.get("summary", "")
                if summary:
                    summary = BeautifulSoup(summary, "html.parser").get_text()[:300]
                
                news_items.append(FetchedNews(
                    ticker=ticker,
                    title=title,
                    source=feed_name.replace("_", " ").title(),
                    url=entry.get("link", ""),
                    published=published,
                    summary=summary or None
                ))
                
        except Exception as e:
            logger.warning(f"RSS fetch failed for {ticker} ({feed_name}): {e}")
        
        return news_items
    
    async def _fetch_rss_url(self, url: str, source_name: str, ticker: str, max_items: int) -> list[FetchedNews]:
        """Fetch news from a direct RSS URL."""
        news_items = []
        
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            feed = feedparser.parse(response.text)
            
            for entry in feed.entries[:max_items]:
                # Parse published date
                published = None
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    try:
                        published = datetime(*entry.published_parsed[:6])
                    except:
                        pass
                
                # Clean title
                title = entry.get("title", "No title")
                if hasattr(title, "replace"):
                    title = BeautifulSoup(title, "html.parser").get_text()
                
                # Get summary
                summary = entry.get("summary", "")
                if summary:
                    summary = BeautifulSoup(summary, "html.parser").get_text()[:300]
                
                news_items.append(FetchedNews(
                    ticker=ticker,
                    title=title,
                    source=source_name.replace("_", " ").title(),
                    url=entry.get("link", ""),
                    published=published,
                    summary=summary or None
                ))
                
        except Exception as e:
            logger.debug(f"RSS URL fetch failed ({source_name}): {e}")
        
        return news_items
    
    async def fetch_multiple_tickers(self, tickers: list[str], max_per_ticker: int = 5) -> list[FetchedNews]:
        """
        Fetch news for multiple tickers concurrently.
        
        Args:
            tickers: List of stock tickers
            max_per_ticker: Max items per ticker
            
        Returns:
            Combined list of news items
        """
        tasks = [self.fetch_for_ticker(t, max_per_ticker) for t in tickers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        all_news = []
        for result in results:
            if isinstance(result, list):
                all_news.extend(result)
            elif isinstance(result, Exception):
                logger.error(f"Fetch error: {result}")
        
        # Sort by published date (newest first)
        all_news.sort(key=lambda x: x.published or datetime.min, reverse=True)
        
        return all_news


# Singleton instance
_fetcher: Optional[NewsFetcher] = None


def get_fetcher() -> NewsFetcher:
    """Get or create singleton fetcher instance."""
    global _fetcher
    if _fetcher is None:
        _fetcher = NewsFetcher()
    return _fetcher
