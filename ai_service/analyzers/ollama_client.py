"""Ollama local AI client - Completely free, runs locally."""

from __future__ import annotations

import logging
from typing import Optional

import requests

from ai_service.config import Settings
from ai_service.analyzers.base_client import BaseAIClient, AIError

logger = logging.getLogger(__name__)


class OllamaClient(BaseAIClient):
    """Client for Ollama - local AI inference, completely free."""
    
    DEFAULT_BASE_URL = "http://localhost:11434"
    
    # Popular Ollama models
    MODEL_FALLBACK_CHAIN = [
        "llama3.1",      # Meta's LLaMA 3.1
        "llama3",        # Meta's LLaMA 3
        "mistral",       # Mistral 7B
        "gemma2",        # Google's Gemma 2
        "phi3",          # Microsoft's Phi-3
    ]
    
    def __init__(self, settings: Optional[Settings] = None):
        """Initialize Ollama client."""
        self.settings = settings or Settings()
        self.base_url = getattr(self.settings, 'ollama_base_url', '') or self.DEFAULT_BASE_URL
        self.default_model = getattr(self.settings, 'ollama_model', '') or "llama3.1"
        
        # Check if Ollama is running
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code != 200:
                raise AIError("Ollama not responding")
            
            # Get available models
            models = response.json().get("models", [])
            self.available_models = [m.get("name", "").split(":")[0] for m in models]
            
            if not self.available_models:
                raise AIError("No Ollama models installed. Run: ollama pull llama3.1")
            
            logger.info(f"Ollama connected. Available models: {self.available_models}")
            
        except requests.exceptions.ConnectionError:
            raise AIError("Ollama not running. Start with: ollama serve")
    
    def generate(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 0.7,
        max_output_tokens: int = 4096,
        max_retries: int = 3,
        model: Optional[str] = None,
    ) -> str:
        """Generate content using Ollama."""
        # Find best available model
        model_to_use = model or self.default_model
        if model_to_use not in self.available_models:
            # Try to find a similar model
            for m in self.MODEL_FALLBACK_CHAIN:
                if m in self.available_models:
                    model_to_use = m
                    break
            else:
                model_to_use = self.available_models[0] if self.available_models else "llama3.1"
        
        # Build prompt
        full_prompt = prompt
        if system_instruction:
            full_prompt = f"{system_instruction}\n\n{prompt}"
        
        payload = {
            "model": model_to_use,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_output_tokens,
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=120  # Longer timeout for local inference
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("response", "")
            else:
                raise AIError(f"Ollama error {response.status_code}: {response.text}")
                
        except requests.exceptions.ConnectionError:
            raise AIError("Ollama connection lost. Check if 'ollama serve' is running.")
        except requests.exceptions.Timeout:
            raise AIError("Ollama request timed out. Model may be too large for your system.")
    
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
