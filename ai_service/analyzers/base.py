"""Base analyzer interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from ai_service.models.article import AnalysisResult, ArticleCollection
from ai_service.pipeline.base import PipelineContext, PipelineStep


class ArticleAnalyzer(PipelineStep[ArticleCollection, AnalysisResult], ABC):
    """Base class for article analyzers."""

    @abstractmethod
    def process(
        self, input_data: ArticleCollection, context: PipelineContext
    ) -> AnalysisResult:
        """Analyze articles and return result."""
        pass
