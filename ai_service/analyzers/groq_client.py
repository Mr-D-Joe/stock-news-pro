"""Groq API client - Fast, free tier AI inference."""

from __future__ import annotations

import logging
import time
from typing import Optional

import requests

from ai_service.config import Settings
from ai_service.analyzers.base_client import BaseAIClient, AIError

logger = logging.getLogger(__name__)


class GroqClient(BaseAIClient):
    """Client for Groq API - extremely fast inference with free tier."""
    
    BASE_URL = "https://api.groq.com/openai/v1/chat/completions"
    
    # Groq models - verified active Jan 2026
    MODEL_FALLBACK_CHAIN = [
        "llama-3.3-70b-versatile",  # Newest, best quality
        "gemma2-9b-it",             # Google's Gemma 2
    ]

    
    def __init__(self, settings: Optional[Settings] = None):
        """Initialize Groq client."""
        self.settings = settings or Settings()
        self.api_key = getattr(self.settings, 'groq_api_key', '') or ''
        self.default_model = "llama-3.3-70b-versatile"
        
        if not self.api_key:
            raise AIError("Groq API key not configured. Get one free at https://console.groq.com")
        
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        })
        
        logger.info(f"Groq client initialized with model: {self.default_model}")
    
    def generate(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 0.7,
        max_output_tokens: int = 4096,
        max_retries: int = 3,
        model: Optional[str] = None,
    ) -> str:
        """Generate content using Groq."""
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})
        
        models_to_try = [model] if model else self.MODEL_FALLBACK_CHAIN
        last_error = None
        
        for model_name in models_to_try:
            try:
                return self._call_api(model_name, messages, temperature, max_output_tokens, max_retries)
            except AIError as e:
                last_error = e
                error_str = str(e).lower()
                if "rate limit" in error_str or "429" in error_str:
                    logger.warning(f"Groq model {model_name} rate limited, trying next...")
                    continue
                raise
        
        raise AIError(f"All Groq models failed. Last error: {last_error}")
    
    def _call_api(self, model: str, messages: list, temperature: float, max_tokens: int, max_retries: int) -> str:
        """Make API call to Groq."""
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        
        for attempt in range(max_retries):
            try:
                response = self.session.post(self.BASE_URL, json=payload, timeout=60)
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("choices", [{}])[0].get("message", {}).get("content", "")
                
                elif response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 5))
                    
                    # Quality over Speed: Wait if within threshold
                    wait_threshold = self.settings.rate_limit_wait_threshold_seconds
                    if retry_after > wait_threshold:
                        logger.warning(f"Groq rate limit wait ({retry_after}s) > {wait_threshold}s. Falling back immediately.")
                        raise AIError("Groq rate limit exceeded (wait too long)")

                    logger.warning(f"Groq rate limited, waiting {retry_after}s...")
                    time.sleep(retry_after)
                    continue
                
                elif response.status_code == 401:
                    raise AIError("Groq API key invalid")
                
                else:
                    error_data = response.json() if response.text else {}
                    error_msg = error_data.get("error", {}).get("message", response.text)
                    raise AIError(f"Groq API error {response.status_code}: {error_msg}")
                    
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                raise AIError("Groq request timed out")
            except requests.exceptions.RequestException as e:
                raise AIError(f"Groq request failed: {e}")
        
        raise AIError(f"Groq max retries exceeded")
    
    def summarize_article(self, title: str, text: str, max_words: int = 100) -> str:
        """Summarize article."""
        prompt = f"Summarize in {max_words} words:\n\nTitle: {title}\n\n{text[:3000]}"
        return self.generate(prompt, temperature=0.3, max_output_tokens=500)
    
    @property
    def on_wait_start(self):
        return self._on_wait_start if hasattr(self, '_on_wait_start') else None
    
    @on_wait_start.setter
    def on_wait_start(self, value):
        self._on_wait_start = value
    
    @property
    def on_wait_tick(self):
        return self._on_wait_tick if hasattr(self, '_on_wait_tick') else None
    
    @on_wait_tick.setter
    def on_wait_tick(self, value):
        self._on_wait_tick = value
