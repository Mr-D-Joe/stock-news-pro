"""Gemini API client for AI analysis."""

from __future__ import annotations

import logging
import time
from datetime import datetime
from typing import Any, Optional, Callable

import requests

from stock_news_ai.config import Settings

from stock_news_ai.analyzers.base_client import BaseAIClient, AIError

logger = logging.getLogger(__name__)


class GeminiError(AIError):
    """Exception for Gemini API errors."""
    pass


class RateLimiter:
    """Simple rate limiter for API calls."""
    
    def __init__(self, requests_per_minute: int = 5):
        self.requests_per_minute = requests_per_minute
        self.min_interval = 60.0 / requests_per_minute  # seconds between requests
        self.last_request_time: Optional[float] = None
    
    def wait_if_needed(self) -> None:
        """Wait if necessary to respect rate limit."""
        if self.last_request_time is None:
            self.last_request_time = time.time()
            return
        
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_interval:
            wait_time = self.min_interval - elapsed
            logger.info(f"Rate limiting: waiting {wait_time:.1f}s before next request")
            time.sleep(wait_time)
        
        self.last_request_time = time.time()


class GeminiClient(BaseAIClient):
    """Client for Google Gemini generative AI API."""

    BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"
    
    # Rate limiter shared across all instances (for free tier: 5 requests/minute)
    _rate_limiter: Optional[RateLimiter] = None

    def __init__(
        self,
        settings: Optional[Settings] = None,
        requests_per_minute: int = 5,  # Free tier limit
    ):
        self.settings = settings or Settings()
        self.api_key = self.settings.gemini_api_key
        self.default_model = self.settings.gemini_model
        self.summary_model = self.settings.gemini_summary_model
        self.fallback_model = "gemini-2.0-flash"  # Standard fallback
        
        # Callbacks for UI integration
        self._on_wait_start: Optional[Callable[[int, bool], None]] = None
        self._on_wait_tick: Optional[Callable[[int], None]] = None
        
        if not self.api_key:
            raise GeminiError("GEMINI_API_KEY is required")
        
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key,
        })
        
        # Initialize rate limiter (shared across instances)
        if GeminiClient._rate_limiter is None:
            GeminiClient._rate_limiter = RateLimiter(requests_per_minute)

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

    def _build_url(self, model: str, action: str = "generateContent") -> str:
        """Build API URL for the specified model and action."""
        return f"{self.BASE_URL}/{model}:{action}"

    def generate(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 0.7,
        max_output_tokens: int = 8192,
        max_retries: int = 5,  # Increased for rate limit handling
        model: Optional[str] = None,  # Use specific model, defaults to gemini_model
    ) -> str:
        """
        Generate content using Gemini.
        
        Args:
            prompt: The user prompt/question
            system_instruction: Optional system-level instruction
            temperature: Creativity level (0-1)
            max_output_tokens: Maximum response length
            max_retries: Number of retry attempts
            model: Specific model to use (defaults to gemini_model from settings)
            
        Returns:
            Generated text response
        """
        use_model = model or self.default_model
        url = self._build_url(use_model, "generateContent")
        
        # Build request body
        body: dict[str, Any] = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_output_tokens,
            },
        }
        
        if system_instruction:
            body["systemInstruction"] = {
                "parts": [{"text": system_instruction}]
            }
        
        # Retry logic with exponential backoff
        last_error: Optional[Exception] = None
        cumulative_wait = 0
        
        for attempt in range(max_retries):
            try:
                # Wait for rate limit before making request
                if GeminiClient._rate_limiter:
                    GeminiClient._rate_limiter.wait_if_needed()
                
                response = self.session.post(url, json=body, timeout=120)
                
                if response.status_code == 429:
                    # Rate limited - extract wait time from API if possible
                    wait_seconds = self._extract_wait_time(response)
                    
                    is_guess = False
                    if wait_seconds is None:
                        # Fallback: parse JSON error details if available
                        wait_seconds = 60 # Default wait for 429
                        is_guess = True
                    
                    # Apply exponential backoff multiplier only if it was a guess
                    if is_guess:
                        wait_seconds = max(wait_seconds, 30) * (attempt + 1)
                    
                    cumulative_wait += wait_seconds
                    
                    msg_prefix = "API-requested" if not is_guess else "Estimated"
                    logger.warning(
                        f"Rate limited (429), {msg_prefix} wait: {wait_seconds}s (Total: {cumulative_wait}s) "
                        f"before retry (attempt {attempt + 1}/{max_retries})"
                    )
                    
                    # Check for fallback if wait is too long (> 10m) OR cumulative wait is already high (> 5m)
                    should_switch = (wait_seconds > 600) or (cumulative_wait > 300)
                    
                    if should_switch and use_model != self.fallback_model:
                        reason = "Wait time > 10m" if wait_seconds > 600 else f"Cumulative wait {cumulative_wait}s > 5m"
                        logger.warning(f"{reason}. Switching to fallback model: {self.fallback_model}")
                        use_model = self.fallback_model
                        url = self._build_url(use_model, "generateContent")
                        # After switching, we don't wait further for the old model's penalty
                        # but we should still respect the new model's rate limit if it ever hits one.
                    else:
                        self._wait_with_feedback(wait_seconds, is_guess)
                    continue
                
                if response.status_code == 503:
                    # Service overloaded - wait and retry
                    wait_time = 20 * (attempt + 1)
                    logger.warning(f"Service overloaded (503), waiting {wait_time}s")
                    self._wait_with_feedback(wait_time, True) # 503 is always a guess
                    continue
                    
                if response.status_code != 200:
                    error_text = response.text[:500]
                    raise GeminiError(f"API error {response.status_code}: {error_text}")
                
                data = response.json()
                return self._extract_text(data)
                
            except requests.RequestException as e:
                last_error = e
                wait_time = 10 * (attempt + 1)
                logger.warning(f"Request failed (attempt {attempt + 1}): {e}, waiting {wait_time}s")
                time.sleep(wait_time)
                continue
        
        raise GeminiError(f"Max retries exceeded: {last_error}")

    def _wait_with_feedback(self, seconds: int, is_guess: bool) -> None:
        """Wait for specified time while providing feedback via callbacks."""
        if self.on_wait_start:
            self.on_wait_start(seconds, is_guess)
            
        for i in range(seconds, 0, -1):
            if self.on_wait_tick:
                self.on_wait_tick(i)
            time.sleep(1)
            
        if self.on_wait_tick:
            self.on_wait_tick(0)

    def _extract_wait_time(self, response: requests.Response) -> Optional[int]:
        """Try to extract wait time from Retry-After header or JSON details."""
        # 1. Try Retry-After header
        retry_after = response.headers.get("Retry-After")
        if retry_after:
            try:
                # Could be digits or a full HTTP date
                if retry_after.isdigit():
                    return int(retry_after)
                
                from email.utils import parsedate_to_datetime
                from datetime import datetime
                dt = parsedate_to_datetime(retry_after)
                delta = (dt - datetime.now(dt.tzinfo)).total_seconds()
                return max(1, int(delta))
            except:
                pass
        
        # 2. Try to parse JSON details for google.rpc.RetryInfo
        try:
            error_data = response.json()
            error = error_data.get("error", {})
            details = error.get("details", [])
            
            for detail in details:
                # Check for RetryInfo
                if detail.get("@type") == "type.googleapis.com/google.rpc.RetryInfo":
                    retry_delay = detail.get("retry_delay", {})
                    seconds = retry_delay.get("seconds")
                    if seconds is not None:
                        return int(seconds)
                
                # Check for ErrorInfo metadata which sometimes contains quotas
                if detail.get("@type") == "type.googleapis.com/google.rpc.ErrorInfo":
                    metadata = detail.get("metadata", {})
                    # Some internal APIs might pass hints here, though rare for Gemini
                    pass
        except:
            pass
            
        return None

    def _extract_text(self, response_data: dict) -> str:
        """Extract text content from API response."""
        try:
            candidates = response_data.get("candidates", [])
            if not candidates:
                raise GeminiError("No candidates in response")
            
            content = candidates[0].get("content", {})
            parts = content.get("parts", [])
            if not parts:
                raise GeminiError("No parts in response content")
            
            return parts[0].get("text", "")
            
        except (KeyError, IndexError) as e:
            raise GeminiError(f"Failed to parse response: {e}")

    def analyze_text(
        self,
        text: str,
        analysis_type: str = "summarize",
    ) -> str:
        """
        Perform specific analysis on text using summary model (higher rate limits).
        
        Args:
            text: Text to analyze
            analysis_type: Type of analysis (summarize, sentiment, extract_facts)
        """
        prompts = {
            "summarize": f"Provide a concise summary of the following text:\n\n{text}",
            "sentiment": f"Analyze the sentiment of the following text. Respond with: POSITIVE, NEGATIVE, or NEUTRAL, followed by a brief explanation.\n\n{text}",
            "extract_facts": f"Extract the key facts and data points from the following text as bullet points:\n\n{text}",
        }
        
        prompt = prompts.get(analysis_type, prompts["summarize"])
        # Use summary_model (gemma-3-27b-it) for better rate limits
        return self.generate(prompt, temperature=0.3, model=self.summary_model)

    def summarize_article(self, title: str, text: str, max_words: int = 100) -> str:
        """
        Summarize a single article using the summary model (gemma-3-27b-it).
        
        This uses a model with higher rate limits, suitable for batch processing.
        
        Args:
            title: Article title
            text: Article text content
            max_words: Maximum words for summary
            
        Returns:
            Concise summary of the article
        """
        prompt = f"""Summarize this news article in approximately {max_words} words.
Focus on key facts, figures, and market implications.

Title: {title}

Content:
{text}

Summary:"""
        
        return self.generate(
            prompt=prompt,
            temperature=0.3,
            max_output_tokens=500,
            model=self.summary_model,  # Uses gemma-3-27b-it
        )
