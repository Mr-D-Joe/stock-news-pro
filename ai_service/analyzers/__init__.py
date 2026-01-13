"""Analyzers package."""

from stock_news_ai.analyzers.base import ArticleAnalyzer
from stock_news_ai.analyzers.essay_generator import EssayGenerator
from stock_news_ai.analyzers.base_client import BaseAIClient, AIError
from stock_news_ai.analyzers.gemini_client import GeminiClient, GeminiError
from stock_news_ai.analyzers.openai_client import OpenAIClient, OpenAIError
from stock_news_ai.analyzers.perplexity_client import PerplexityClient, PerplexityError
from stock_news_ai.analyzers.provider_factory import ProviderFactory
from stock_news_ai.analyzers.prompts import (
    SYSTEM_INSTRUCTION_ANALYST,
    build_anomaly_detection_prompt,
    build_essay_prompt,
    build_summary_prompt,
)

__all__ = [
    "ArticleAnalyzer",
    "EssayGenerator",
    "BaseAIClient",
    "AIError",
    "GeminiClient",
    "GeminiError",
    "OpenAIClient",
    "OpenAIError",
    "PerplexityClient",
    "PerplexityError",
    "ProviderFactory",
    "SYSTEM_INSTRUCTION_ANALYST",
    "build_anomaly_detection_prompt",
    "build_essay_prompt",
    "build_summary_prompt",
]
