"""Base analyzer interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from stock_news_ai.models.article import AnalysisResult, ArticleCollection
from stock_news_ai.pipeline.base import PipelineContext, PipelineStep


class ArticleAnalyzer(PipelineStep[ArticleCollection, AnalysisResult], ABC):
    """Base class for article analyzers."""

    @abstractmethod
    def process(
        self, input_data: ArticleCollection, context: PipelineContext
    ) -> AnalysisResult:
        """Analyze articles and return result."""
        pass
