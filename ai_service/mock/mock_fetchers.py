"""Mock fetchers for development mode - no external API calls."""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass

from ai_service.mock.mock_data import (
    MOCK_STOCKS,
    MOCK_FUNDAMENTALS,
    get_mock_news,
    get_mock_deep_web,
    get_mock_price_data,
    get_mock_events,
)
from ai_service.models.contracts import FundamentalsData, PriceHistoryResult, EventItem, StockResolution, DeepWebSource

logger = logging.getLogger(__name__)


@dataclass
class MockFetchedNews:
    """Mock news item matching FetchedNews interface."""
    ticker: str
    title: str
    source: str
    url: Optional[str] = None
    published: Optional[datetime] = None
    summary: Optional[str] = None


class MockNewsFetcher:
    """Mock news fetcher that returns predefined news for mock stocks.
    
    Implements same interface as NewsFetcher but uses mock data.
    """
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self._seen_sources: set = set()
        logger.info("MockNewsFetcher initialized - NO external API calls will be made")
    
    async def fetch_for_ticker(self, ticker: str, max_items: int = 30) -> List[MockFetchedNews]:
        """Fetch mock news for a ticker.
        
        Args:
            ticker: Stock ticker symbol
            max_items: Maximum number of items to return
            
        Returns:
            List of MockFetchedNews objects
        """
        logger.info(f"MockNewsFetcher: Fetching news for {ticker} (max: {max_items})")
        
        # Get mock news data
        news_data = get_mock_news(ticker.upper())
        
        if not news_data:
            logger.warning(f"MockNewsFetcher: No mock data for ticker {ticker}")
            # Return generic news for unknown tickers
            return [
                MockFetchedNews(
                    ticker=ticker,
                    title=f"{ticker} Stock Update",
                    source="MockNews",
                    url=f"https://mock.news/{ticker.lower()}",
                    published=datetime.now() - timedelta(days=1),
                    summary=f"Latest developments for {ticker}."
                )
            ]
        
        # Convert to MockFetchedNews objects
        result: List[MockFetchedNews] = []
        for item in news_data[:max_items]:
            result.append(MockFetchedNews(
                ticker=ticker,
                title=item["title"],
                source=item["source"],
                url=item.get("url", f"https://mock.news/{ticker.lower()}/{len(result)}"),
                published=item["published"],
                summary=item.get("summary", "")
            ))
        
        logger.info(f"MockNewsFetcher: Returned {len(result)} mock news items for {ticker}")
        return result
    
    async def fetch_multiple_tickers(
        self, tickers: List[str], max_per_ticker: int = 5
    ) -> List[MockFetchedNews]:
        """Fetch news for multiple tickers.
        
        Args:
            tickers: List of stock tickers
            max_per_ticker: Max items per ticker
            
        Returns:
            Combined list of news items
        """
        all_news = []
        for ticker in tickers:
            news = await self.fetch_for_ticker(ticker, max_per_ticker)
            all_news.extend(news)
        return all_news


class MockHistoricAnalyzer:
    """Mock historic analyzer with predefined price and fundamental data.
    
    Implements same interface as HistoricAnalyzer but uses mock data.
    """
    
    def __init__(self, settings=None):
        self.settings = settings
        self._client = None  # Not used in mock
        logger.info("MockHistoricAnalyzer initialized - NO external API calls will be made")
    
    async def get_fundamentals(self, ticker: str) -> FundamentalsData:
        """Get mock fundamental data for a ticker.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Dictionary with fundamental metrics
        """
        logger.info(f"MockHistoricAnalyzer: Getting fundamentals for {ticker}")
        
        fundamentals = MOCK_FUNDAMENTALS.get(ticker.upper())
        
        if not fundamentals:
            logger.warning(f"MockHistoricAnalyzer: No mock fundamentals for {ticker}, using defaults")
            return {
                "pe_ratio": 20.0,
                "peg_ratio": 1.5,
                "roe": 15.0,
                "debt_to_equity": 0.5,
                "target_mean_price": 100.0,
                "recommendation": "hold",
                "business_summary": f"Mock company data for {ticker}.",
                "sector": "Unknown",
            }
        
        logger.info(f"MockHistoricAnalyzer: Returned fundamentals for {ticker}")
        return fundamentals.copy()
    
    async def get_price_data(self, ticker: str, period: str = "10y") -> PriceHistoryResult:
        """Get mock price history for a ticker.
        
        Args:
            ticker: Stock ticker symbol
            period: Time period (1d, 1wk, 1mo, 3mo, 6mo, 1y, 10y)
            
        Returns:
            Dictionary with price data
        """
        logger.info(f"MockHistoricAnalyzer: Getting price data for {ticker} ({period})")
        
        price_data = get_mock_price_data(ticker.upper(), period)
        
        logger.info(f"MockHistoricAnalyzer: Returned {len(price_data.get('data', []))} price points")
        return price_data
    
    def slice_periods(
        self, full_data: PriceHistoryResult, periods: List[str]
    ) -> Dict[str, PriceHistoryResult]:
        """Slice full price data into smaller periods.
        
        Args:
            full_data: Complete price data
            periods: List of periods to slice
            
        Returns:
            Dict mapping period -> price_data
        """
        result: Dict[str, PriceHistoryResult] = {}
        data = full_data.get("data", [])
        
        if not data:
            return {p: {"data": [], "ticker": full_data.get("ticker", "")} for p in periods}
        
        period_days = {
            "10y": 3650, "5y": 1825, "1y": 365, "6mo": 180,
            "3mo": 90, "1mo": 30, "1wk": 7, "1d": 1, "24h": 1
        }
        
        now = datetime.now()
        
        for period in periods:
            days = period_days.get(period, 365)
            cutoff = now - timedelta(days=days)
            
            filtered = []
            for d in data:
                try:
                    date_str = d["date"].replace("Z", "").replace("+00:00", "")
                    if "T" not in date_str:
                        date_str += "T00:00:00"
                    point_date = datetime.fromisoformat(date_str)
                    if point_date >= cutoff:
                        filtered.append(d)
                except (ValueError, KeyError):
                    continue
            
            result[period] = {
                "ticker": full_data.get("ticker", ""),
                "period": period,
                "data": filtered,
                "last_price": filtered[-1]["close"] if filtered else 0,
                "source": "mock"
            }
        
        return result
    
    async def identify_pivotal_events(
        self, ticker: str, company_name: str
    ) -> List[EventItem]:
        """Get mock pivotal events for a ticker.
        
        Args:
            ticker: Stock ticker symbol
            company_name: Company name
            
        Returns:
            List of event dictionaries
        """
        logger.info(f"MockHistoricAnalyzer: Getting events for {ticker}")
        events = get_mock_events(ticker.upper())
        logger.info(f"MockHistoricAnalyzer: Returned {len(events)} mock events")
        return events


class MockDeepCollector:
    """Mock deep web collector that returns predefined deep sources.
    
    Implements same interface as DeepCollector but uses mock data.
    """
    
    def __init__(self, settings=None):
        self.settings = settings
        logger.info("MockDeepCollector initialized - NO external API calls will be made")
    
    async def collect(
        self, ticker: str, company_name: str, limit: int = 6
    ) -> List[DeepWebSource]:
        """Collect mock deep web sources for a ticker.
        
        Args:
            ticker: Stock ticker symbol
            company_name: Company name
            limit: Maximum number of sources
            
        Returns:
            List of deep web source dictionaries
        """
        logger.info(f"MockDeepCollector: Collecting deep sources for {ticker} ({company_name})")
        
        deep_data = get_mock_deep_web(ticker.upper())
        
        if not deep_data:
            logger.warning(f"MockDeepCollector: No mock deep data for {ticker}")
            return []
        
        result = deep_data[:limit]
        logger.info(f"MockDeepCollector: Returned {len(result)} mock deep sources")
        return result


class MockTickerResolver:
    """Mock ticker resolver for development mode."""
    
    def __init__(self, settings=None):
        self.settings = settings
        logger.info("MockTickerResolver initialized - NO external API calls will be made")
    
    async def resolve_stock(self, query: str) -> StockResolution:
        """Resolve a stock query to ticker info.
        
        Args:
            query: Stock ticker or name
            
        Returns:
            Dictionary with symbol, name, sector
        """
        query_upper = query.upper().strip()
        
        # Check if it's a known mock stock
        if query_upper in MOCK_STOCKS:
            stock = MOCK_STOCKS[query_upper]
            return {
                "symbol": stock["symbol"],
                "name": stock["name"],
                "sector": stock["sector"],
                "found": True
            }
        
        # Check by name
        for symbol, stock in MOCK_STOCKS.items():
            if query.lower() in stock["name"].lower():
                return {
                    "symbol": stock["symbol"],
                    "name": stock["name"],
                    "sector": stock["sector"],
                    "found": True
                }
        
        # Return query as-is for unknown stocks
        return {
            "symbol": query_upper,
            "name": query,
            "sector": "Unknown",
            "found": False
        }
    
    async def resolve_sector(self, query: str) -> str:
        """Resolve a sector name."""
        sector_map = {
            "tech": "Technology",
            "bio": "Healthcare",
            "biotech": "Healthcare",
            "energy": "Energy",
            "finance": "Financials",
            "fintech": "Financials",
        }
        return sector_map.get(query.lower(), query)


# =============================================================================
# FACTORY FUNCTIONS
# =============================================================================

_mock_fetcher: Optional[MockNewsFetcher] = None
_mock_historic: Optional[MockHistoricAnalyzer] = None
_mock_deep: Optional[MockDeepCollector] = None
_mock_resolver: Optional[MockTickerResolver] = None


def get_mock_fetcher() -> MockNewsFetcher:
    """Get or create singleton mock fetcher instance."""
    global _mock_fetcher
    if _mock_fetcher is None:
        _mock_fetcher = MockNewsFetcher()
    return _mock_fetcher


def get_mock_historic_analyzer(settings=None) -> MockHistoricAnalyzer:
    """Get or create singleton mock historic analyzer instance."""
    global _mock_historic
    if _mock_historic is None:
        _mock_historic = MockHistoricAnalyzer(settings)
    return _mock_historic


def get_mock_deep_collector(settings=None) -> MockDeepCollector:
    """Get or create singleton mock deep collector instance."""
    global _mock_deep
    if _mock_deep is None:
        _mock_deep = MockDeepCollector(settings)
    return _mock_deep


def get_mock_ticker_resolver(settings=None) -> MockTickerResolver:
    """Get or create singleton mock ticker resolver instance."""
    global _mock_resolver
    if _mock_resolver is None:
        _mock_resolver = MockTickerResolver(settings)
    return _mock_resolver
