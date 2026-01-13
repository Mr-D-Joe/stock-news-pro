"""OpenAI API client for AI analysis."""

from __future__ import annotations

import logging
import time
from typing import Any, Optional, Callable

import requests

from stock_news_ai.analyzers.base_client import BaseAIClient, AIError
from stock_news_ai.config import Settings

logger = logging.getLogger(__name__)


class OpenAIError(AIError):
    """Exception for OpenAI API errors."""
    pass


class OpenAIClient(BaseAIClient):
    """Client for OpenAI API."""

    BASE_URL = "https://api.openai.com/v1"

    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        self.api_key = self.settings.openai_api_key
        self.default_model = self.settings.openai_model
        
        self._on_wait_start: Optional[Callable[[int, bool], None]] = None
        self._on_wait_tick: Optional[Callable[[int], None]] = None
        
        if not self.api_key:
            # We don't raise here yet, as it might be an optional provider
            logger.warning("OPENAI_API_KEY is not set")
        
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        })

    @property
    def on_wait_start(self) -> Optional[Callable[[int, bool], None]]:
        return self._on_wait_start

    @on_wait_start.setter
    def on_wait_start(self, value: Optional[Callable[[int, bool], None]]) -> None:
        self._on_wait_start = value

    @property
    def on_wait_tick(self) -> Optional[Callable[[int], None]]:
        return self._on_wait_tick

    @on_wait_tick.setter
    def on_wait_tick(self, value: Optional[Callable[[int], None]]) -> None:
        self._on_wait_tick = value

    def generate(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 0.7,
        max_output_tokens: int = 4096,
        max_retries: int = 3,
        model: Optional[str] = None,
    ) -> str:
        """Generate content using OpenAI."""
        if not self.api_key:
            raise OpenAIError("OPENAI_API_KEY is missing")

        use_model = model or self.default_model
        url = f"{self.BASE_URL}/chat/completions"
        
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})
        
        body = {
            "model": use_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_output_tokens,
        }
        
        for attempt in range(max_retries):
            try:
                response = self.session.post(url, json=body, timeout=120)
                
                if response.status_code == 429:
                    wait_time = 30 * (attempt + 1)
                    logger.warning(f"OpenAI Rate limit, waiting {wait_time}s")
                    self._wait_with_feedback(wait_time, True)
                    continue
                    
                if response.status_code != 200:
                    raise OpenAIError(f"OpenAI error {response.status_code}: {response.text}")
                
                data = response.json()
                return data["choices"][0]["message"]["content"].strip()
                
            except requests.RequestException as e:
                wait_time = 10 * (attempt + 1)
                logger.warning(f"OpenAI request failed: {e}, retrying in {wait_time}s")
                time.sleep(wait_time)
                continue
                
        raise OpenAIError("Max retries exceeded for OpenAI")

    def _wait_with_feedback(self, seconds: int, is_guess: bool) -> None:
        if self.on_wait_start:
            self.on_wait_start(seconds, is_guess)
        for i in range(seconds, 0, -1):
            if self.on_wait_tick:
                self.on_wait_tick(i)
            time.sleep(1)
        if self.on_wait_tick:
            self.on_wait_tick(0)

    def summarize_article(self, title: str, text: str, max_words: int = 100) -> str:
        prompt = f"Summarize the following article in about {max_words} words:\n\nTitle: {title}\n\nContent: {text}"
        return self.generate(prompt, temperature=0.3)
