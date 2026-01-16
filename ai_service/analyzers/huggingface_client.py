"""HuggingFace Inference API client - Free tier with various models."""

from __future__ import annotations

import logging
import time
from typing import Optional

import requests

from ai_service.config import Settings
from ai_service.analyzers.base_client import BaseAIClient, AIError

logger = logging.getLogger(__name__)


class HuggingFaceClient(BaseAIClient):
    """Client for HuggingFace Inference API - free tier available."""
    
    BASE_URL = "https://api-inference.huggingface.co/models"
    
    # Free models that work well for text generation
    MODEL_FALLBACK_CHAIN = [
        "mistralai/Mistral-7B-Instruct-v0.2",
        "google/gemma-7b-it",
        "HuggingFaceH4/zephyr-7b-beta",
        "tiiuae/falcon-7b-instruct",
    ]
    
    def __init__(self, settings: Optional[Settings] = None):
        """Initialize HuggingFace client."""
        self.settings = settings or Settings()
        self.api_key = getattr(self.settings, 'huggingface_api_key', '') or ''
        self.default_model = "mistralai/Mistral-7B-Instruct-v0.2"
        
        if not self.api_key:
            raise AIError("HuggingFace API key not configured. Get one free at https://huggingface.co/settings/tokens")
        
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        })
        
        logger.info(f"HuggingFace client initialized with model: {self.default_model}")
    
    def generate(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 0.7,
        max_output_tokens: int = 2048,
        max_retries: int = 3,
        model: Optional[str] = None,
    ) -> str:
        """Generate content using HuggingFace Inference API."""
        # Format prompt for instruction-tuned models
        full_prompt = prompt
        if system_instruction:
            full_prompt = f"[INST] {system_instruction}\n\n{prompt} [/INST]"
        else:
            full_prompt = f"[INST] {prompt} [/INST]"
        
        models_to_try = [model] if model else self.MODEL_FALLBACK_CHAIN
        last_error = None
        
        for model_name in models_to_try:
            try:
                return self._call_api(model_name, full_prompt, temperature, max_output_tokens, max_retries)
            except AIError as e:
                last_error = e
                error_str = str(e).lower()
                if "loading" in error_str or "rate" in error_str or "503" in error_str:
                    logger.warning(f"HuggingFace model {model_name} unavailable, trying next...")
                    continue
                raise
        
        raise AIError(f"All HuggingFace models failed. Last error: {last_error}")
    
    def _call_api(self, model: str, prompt: str, temperature: float, max_tokens: int, max_retries: int) -> str:
        """Make API call to HuggingFace."""
        url = f"{self.BASE_URL}/{model}"
        payload = {
            "inputs": prompt,
            "parameters": {
                "temperature": temperature,
                "max_new_tokens": min(max_tokens, 2048),  # HF has lower limits
                "return_full_text": False,
            },
            "options": {
                "wait_for_model": True,  # Wait if model is loading
            }
        }
        
        for attempt in range(max_retries):
            try:
                response = self.session.post(url, json=payload, timeout=120)
                
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, list) and len(data) > 0:
                        return data[0].get("generated_text", "")
                    return str(data)
                
                elif response.status_code == 503:
                    # Model is loading
                    estimated_time = response.json().get("estimated_time", 30)
                    logger.info(f"HuggingFace model loading, waiting {estimated_time}s...")
                    time.sleep(min(estimated_time, 30))
                    continue
                
                elif response.status_code == 429:
                    logger.warning("HuggingFace rate limited, waiting 10s...")
                    time.sleep(10)
                    continue
                
                elif response.status_code == 401:
                    raise AIError("HuggingFace API key invalid")
                
                else:
                    raise AIError(f"HuggingFace error {response.status_code}: {response.text[:200]}")
                    
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    time.sleep(5)
                    continue
                raise AIError("HuggingFace request timed out")
            except requests.exceptions.RequestException as e:
                raise AIError(f"HuggingFace request failed: {e}")
        
        raise AIError("HuggingFace max retries exceeded")
    
    def summarize_article(self, title: str, text: str, max_words: int = 100) -> str:
        """Summarize article."""
        prompt = f"Summarize in {max_words} words:\n\nTitle: {title}\n\n{text[:2000]}"
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
