"""OpenAI API client for AI analysis - Fallback provider when Gemini is rate-limited."""

from __future__ import annotations

import logging
import time
import random
from typing import Optional

import requests

from ai_service.config import Settings
from ai_service.analyzers.base_client import BaseAIClient, AIError

logger = logging.getLogger(__name__)


class OpenAIClient(BaseAIClient):
    """Client for OpenAI GPT models with automatic model fallback."""
    
    BASE_URL = "https://api.openai.com/v1/chat/completions"
    
    # Fallback chain: Start with best, fall back to cheaper/more available models
    MODEL_FALLBACK_CHAIN = [
        "gpt-4o-mini",      # Best cost/performance ratio
        "gpt-4o",           # Most capable
        "gpt-4-turbo",      # Previous generation
        "gpt-3.5-turbo",    # Cheapest, most reliable
    ]
    
    # Proactive rate limiting (shared across instances)
    _last_request_time: float = 0
    _min_interval: float = 3.0  # 20 RPM = 3 seconds minimum between requests
    
    def __init__(self, settings: Optional[Settings] = None):
        """Initialize OpenAI client."""
        self.settings = settings or Settings()
        self.api_key = self.settings.openai_api_key
        self.default_model = self.settings.openai_model or "gpt-4o-mini"
        
        if not self.api_key:
            raise AIError("OpenAI API key not configured")
        
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        })
        
        logger.info(f"OpenAI client initialized with model: {self.default_model}")
    
    def generate(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 0.7,
        max_output_tokens: int = 4096,
        max_retries: int = 3,
        model: Optional[str] = None,
    ) -> str:
        """
        Generate content using OpenAI GPT models.
        
        Args:
            prompt: The user prompt/question
            system_instruction: Optional system-level instruction
            temperature: Creativity level (0-2)
            max_output_tokens: Maximum tokens for response
            max_retries: Number of retries on failure
            model: Specific model to use (default: use fallback chain)
            
        Returns:
            Generated text response
        """
        # Build messages
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})
        
        # Determine models to try
        if model:
            models_to_try = [model]
        else:
            # Start with default, then try fallback chain
            models_to_try = [self.default_model] + [
                m for m in self.MODEL_FALLBACK_CHAIN if m != self.default_model
            ]
        
        last_error = None
        
        for model_name in models_to_try:
            try:
                result = self._call_api(
                    model=model_name,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_output_tokens,
                    max_retries=max_retries,
                )
                return result
            except AIError as e:
                last_error = e
                error_str = str(e).lower()
                
                # Check if we should try next model
                if "rate limit" in error_str or "quota" in error_str or "429" in error_str:
                    logger.warning(f"OpenAI model {model_name} rate limited, trying next...")
                    continue
                elif "model" in error_str and "not found" in error_str:
                    logger.warning(f"OpenAI model {model_name} not available, trying next...")
                    continue
                else:
                    # Non-recoverable error
                    raise
        
        # All models failed
        raise AIError(f"All OpenAI models failed. Last error: {last_error}")
    
    def _call_api(
        self,
        model: str,
        messages: list,
        temperature: float,
        max_tokens: int,
        max_retries: int,
    ) -> str:
        """Make actual API call to OpenAI."""
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        
        for attempt in range(max_retries):
            try:
                # Proactive rate limiting - avoid hitting limits
                elapsed = time.time() - OpenAIClient._last_request_time
                if elapsed < OpenAIClient._min_interval:
                    sleep_time = OpenAIClient._min_interval - elapsed
                    logger.debug(f"Proactive rate limit: waiting {sleep_time:.1f}s")
                    time.sleep(sleep_time)
                OpenAIClient._last_request_time = time.time()
                
                response = self.session.post(
                    self.BASE_URL,
                    json=payload,
                    timeout=120,
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return self._extract_text(data)
                
                elif response.status_code == 429:
                    # Rate limited - exponential backoff with jitter
                    retry_after = int(response.headers.get("Retry-After", 5))
                    # Exponential backoff: base * 2^attempt with jitter (±25%)
                    exponential_factor = 2 ** min(attempt, 4)  # Cap at 16x
                    jitter = 0.75 + 0.5 * random.random()  # 0.75 - 1.25
                    wait_time = min(retry_after * exponential_factor * jitter, 120)  # Max 2 min
                    logger.warning(f"OpenAI rate limited, waiting {wait_time:.1f}s (attempt {attempt+1})...")
                    time.sleep(wait_time)
                    continue
                
                elif response.status_code == 401:
                    raise AIError("OpenAI API key invalid or expired")
                
                elif response.status_code == 404:
                    raise AIError(f"OpenAI model '{model}' not found")
                
                else:
                    error_data = response.json() if response.text else {}
                    error_msg = error_data.get("error", {}).get("message", response.text)
                    raise AIError(f"OpenAI API error {response.status_code}: {error_msg}")
                    
            except requests.exceptions.Timeout:
                logger.warning(f"OpenAI request timeout (attempt {attempt + 1})")
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                raise AIError("OpenAI request timed out")
            
            except requests.exceptions.RequestException as e:
                raise AIError(f"OpenAI request failed: {e}")
        
        raise AIError(f"OpenAI max retries ({max_retries}) exceeded")
    
    def _extract_text(self, response_data: dict) -> str:
        """Extract text content from API response."""
        try:
            choices = response_data.get("choices", [])
            if choices:
                return choices[0].get("message", {}).get("content", "")
            return ""
        except Exception as e:
            logger.error(f"Failed to extract OpenAI response: {e}")
            return ""
    
    def analyze_text(self, text: str, analysis_type: str = "summarize") -> str:
        """Analyze text using OpenAI."""
        prompts = {
            "summarize": f"Summarize the following text concisely:\n\n{text}",
            "sentiment": f"Analyze the sentiment of this text (positive/negative/neutral) and explain:\n\n{text}",
            "extract_facts": f"Extract key facts and data points from this text:\n\n{text}",
        }
        prompt = prompts.get(analysis_type, prompts["summarize"])
        return self.generate(prompt, temperature=0.3)
    
    def summarize_article(self, title: str, text: str, max_words: int = 100) -> str:
        """Summarize a single article."""
        prompt = f"""Summarize this article in {max_words} words or less.

Title: {title}

{text[:3000]}"""
        
        return self.generate(prompt, temperature=0.3, max_output_tokens=500)
    
    # Implement required abstract properties for callback support
    @property
    def on_wait_start(self):
        """Callback when waiting starts."""
        return self._on_wait_start if hasattr(self, '_on_wait_start') else None
    
    @on_wait_start.setter
    def on_wait_start(self, value):
        """Set callback for when waiting starts."""
        self._on_wait_start = value
    
    @property
    def on_wait_tick(self):
        """Callback for each second of waiting."""
        return self._on_wait_tick if hasattr(self, '_on_wait_tick') else None
    
    @on_wait_tick.setter
    def on_wait_tick(self, value):
        """Set callback for each second of waiting."""
        self._on_wait_tick = value
