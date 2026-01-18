"""Mock module for development mode - complete mock environment.

When DEV_MODE=true, this module provides mock implementations for:
- AI Client (MockAIClient)
- News Fetcher (MockNewsFetcher)
- Historic Analyzer (MockHistoricAnalyzer)
- Deep Web Collector (MockDeepCollector)
- Ticker Resolver (MockTickerResolver)

All classes return predefined data without making external API calls.
"""

# Mock data exports
from ai_service.mock.mock_data import (
    MOCK_STOCKS,
    MOCK_FUNDAMENTALS,
    MOCK_ANALYSIS,
    get_mock_news,
    get_mock_deep_web,
    get_mock_price_data,
    get_mock_analysis,
    get_mock_events,
)

# Mock AI client export
from ai_service.mock.mock_ai_client import MockAIClient

# Mock fetcher exports
from ai_service.mock.mock_fetchers import (
    MockNewsFetcher,
    MockHistoricAnalyzer,
    MockDeepCollector,
    MockTickerResolver,
    MockFetchedNews,
    get_mock_fetcher,
    get_mock_historic_analyzer,
    get_mock_deep_collector,
    get_mock_ticker_resolver,
)

__all__ = [
    # Data
    "MOCK_STOCKS",
    "MOCK_FUNDAMENTALS",
    "MOCK_ANALYSIS",
    "get_mock_news",
    "get_mock_deep_web",
    "get_mock_price_data",
    "get_mock_analysis",
    "get_mock_events",
    # AI Client
    "MockAIClient",
    # Fetchers
    "MockNewsFetcher",
    "MockHistoricAnalyzer",
    "MockDeepCollector",
    "MockTickerResolver",
    "MockFetchedNews",
    # Factory functions
    "get_mock_fetcher",
    "get_mock_historic_analyzer",
    "get_mock_deep_collector",
    "get_mock_ticker_resolver",
]
