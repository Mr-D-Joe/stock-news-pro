"""Analyzers package."""

from ai_service.analyzers.base import ArticleAnalyzer
from ai_service.analyzers.essay_generator import EssayGenerator
from ai_service.analyzers.base_client import BaseAIClient, AIError
from ai_service.analyzers.gemini_client import GeminiClient, GeminiError
from ai_service.analyzers.openai_client import OpenAIClient
from ai_service.analyzers.perplexity_client import PerplexityClient
from ai_service.analyzers.provider_factory import ProviderFactory
from ai_service.analyzers.prompts import (
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
    "PerplexityClient",
    "ProviderFactory",
    "SYSTEM_INSTRUCTION_ANALYST",
    "build_anomaly_detection_prompt",
    "build_essay_prompt",
    "build_summary_prompt",
]
