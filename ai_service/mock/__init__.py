"""Mock module for development mode."""

from ai_service.mock.mock_data import (
    MOCK_STOCKS,
    MOCK_FUNDAMENTALS,
    get_mock_news,
    get_mock_deep_web,
    get_mock_price_data,
    get_mock_analysis,
)
from ai_service.mock.mock_ai_client import MockAIClient

__all__ = [
    "MOCK_STOCKS",
    "MOCK_FUNDAMENTALS",
    "get_mock_news",
    "get_mock_deep_web",
    "get_mock_price_data",
    "get_mock_analysis",
    "MockAIClient",
]
