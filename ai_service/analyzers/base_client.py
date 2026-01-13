"""Base interface for AI clients."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Callable


class AIError(Exception):
    """Base exception for AI client errors."""
    pass


class BaseAIClient(ABC):
    """Abstract base class for all AI providers."""

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 0.7,
        max_output_tokens: int = 8192,
        max_retries: int = 5,
        model: Optional[str] = None,
    ) -> str:
        """Generate content using the AI provider."""
        pass

    @abstractmethod
    def summarize_article(self, title: str, text: str, max_words: int = 100) -> str:
        """Summarize a single article."""
        pass

    @property
    @abstractmethod
    def on_wait_start(self) -> Optional[Callable[[int, bool], None]]:
        """Callback when waiting starts."""
        pass

    @on_wait_start.setter
    @abstractmethod
    def on_wait_start(self, value: Optional[Callable[[int, bool], None]]) -> None:
        """Set callback for when waiting starts."""
        pass

    @property
    @abstractmethod
    def on_wait_tick(self) -> Optional[Callable[[int], None]]:
        """Callback for each second of waiting."""
        pass

    @on_wait_tick.setter
    @abstractmethod
    def on_wait_tick(self, value: Optional[Callable[[int], None]]) -> None:
        """Set callback for each second of waiting."""
        pass
