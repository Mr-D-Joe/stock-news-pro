"""Factory for creating AI clients."""

from __future__ import annotations

import logging
from typing import Optional

from stock_news_ai.analyzers.base_client import BaseAIClient
from stock_news_ai.analyzers.gemini_client import GeminiClient
from stock_news_ai.analyzers.openai_client import OpenAIClient
from stock_news_ai.analyzers.perplexity_client import PerplexityClient
from stock_news_ai.config import Settings

logger = logging.getLogger(__name__)


class ProviderFactory:
    """Factory for AI provider clients."""

    @staticmethod
    def get_client(provider: str = "gemini", settings: Optional[Settings] = None) -> BaseAIClient:
        """
        Get an AI client based on the provider name.
        
        Args:
            provider: 'gemini', 'openai', or 'perplexity'
            settings: Optional application settings
        """
        settings = settings or Settings()
        
        p_lower = provider.lower()
        if p_lower == "openai":
            if not settings.openai_api_key:
                logger.warning("OpenAI requested but key is missing, falling back to Gemini")
                return GeminiClient(settings)
            return OpenAIClient(settings)
        elif p_lower == "perplexity":
            if not settings.perplexity_api_key:
                logger.warning("Perplexity requested but key is missing, falling back to Gemini")
                return GeminiClient(settings)
            return PerplexityClient(settings)
        
        # Default to Gemini
        return GeminiClient(settings)

    @staticmethod
    def get_best_available_client(settings: Optional[Settings] = None) -> BaseAIClient:
        """Try to get OpenAI first, then Gemini (or as configured)."""
        settings = settings or Settings()
        if settings.openai_api_key:
            return OpenAIClient(settings)
        return GeminiClient(settings)
