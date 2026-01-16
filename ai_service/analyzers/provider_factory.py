"""Factory for creating AI clients with automatic fallback support."""

from __future__ import annotations

import logging
from typing import Optional

from ai_service.analyzers.base_client import BaseAIClient, AIError
from ai_service.analyzers.gemini_client import GeminiClient
from ai_service.config import Settings

logger = logging.getLogger(__name__)


class FallbackClient(BaseAIClient):
    """AI client that automatically falls back between providers on failure."""
    
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        self._clients = []
        
        # Initialize available clients in priority order
        # Priority: OpenAI (primary, reliable) > Gemini (fast, free tier)
        # DISABLED: Groq, OpenRouter, HuggingFace, Ollama (per user request)
        
        # 1. OpenAI (PRIMARY - reliable, high quality)
        if self.settings.openai_api_key:
            try:
                from ai_service.analyzers.openai_client import OpenAIClient
                self._clients.append(("OpenAI", OpenAIClient(self.settings)))
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI: {e}")
        
        # 2. Gemini (secondary - fast, free tier available)
        if self.settings.gemini_api_key:
            try:
                self._clients.append(("Gemini", GeminiClient(self.settings)))
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini: {e}")
        
        # NOTE: Groq, OpenRouter, HuggingFace, Ollama are DISABLED
        # to reduce unnecessary API calls and focus on reliable providers
        
        if not self._clients:
            raise AIError("No AI providers configured. Add OPENAI_API_KEY or GEMINI_API_KEY to .env")
        
        logger.info(f"FallbackClient initialized with {len(self._clients)} providers: {[c[0] for c in self._clients]}")
    
    def generate(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 0.7,
        max_output_tokens: int = 8192,
        max_retries: int = 3,
        model: Optional[str] = None,
    ) -> str:
        """Generate content, automatically falling back between providers."""
        last_error = None
        
        # Premium providers (worth waiting for)
        premium_providers = {"Gemini", "Groq", "OpenAI"}
        
        for provider_name, client in self._clients:
            try:
                logger.info(f"Trying {provider_name}...")
                
                # Premium providers: allow retries so they can wait for rate limit
                # Cheap providers: fail fast to move to next
                provider_retries = 3 if provider_name in premium_providers else 1
                
                result = client.generate(
                    prompt=prompt,
                    system_instruction=system_instruction,
                    temperature=temperature,
                    max_output_tokens=max_output_tokens,
                    max_retries=provider_retries,
                )
                logger.info(f"Successfully generated via {provider_name}")
                return result
                
            except AIError as e:
                last_error = e
                error_str = str(e).lower()
                
                # Check if we should fallback
                if any(term in error_str for term in ["rate limit", "quota", "429", "resource_exhausted"]):
                    logger.warning(f"{provider_name} rate limited, falling back to next provider...")
                    continue
                elif "max retries" in error_str:
                    logger.warning(f"{provider_name} max retries exceeded, falling back...")
                    continue
                else:
                    # For other errors, also try fallback
                    logger.warning(f"{provider_name} failed: {e}, trying next provider...")
                    continue
            
            except Exception as e:
                last_error = AIError(str(e))
                logger.warning(f"{provider_name} unexpected error: {e}, trying next provider...")
                continue
        
        # All providers failed
        raise AIError(f"All AI providers failed. Last error: {last_error}")
    
    def analyze_text(self, text: str, analysis_type: str = "summarize") -> str:
        """Analyze text using available provider."""
        prompts = {
            "summarize": f"Summarize the following text concisely:\n\n{text}",
            "sentiment": f"Analyze the sentiment of this text:\n\n{text}",
            "extract_facts": f"Extract key facts from this text:\n\n{text}",
        }
        prompt = prompts.get(analysis_type, prompts["summarize"])
        return self.generate(prompt, temperature=0.3)
    
    def summarize_article(self, title: str, text: str, max_words: int = 100) -> str:
        """Summarize article using available provider."""
        prompt = f"Summarize in {max_words} words:\n\nTitle: {title}\n\n{text[:3000]}"
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
        # Propagate to all clients
        for _, client in self._clients:
            if hasattr(client, 'on_wait_start'):
                client.on_wait_start = value
    
    @property
    def on_wait_tick(self):
        """Callback for each second of waiting."""
        return self._on_wait_tick if hasattr(self, '_on_wait_tick') else None
    
    @on_wait_tick.setter
    def on_wait_tick(self, value):
        """Set callback for each second of waiting."""
        self._on_wait_tick = value
        # Propagate to all clients
        for _, client in self._clients:
            if hasattr(client, 'on_wait_tick'):
                client.on_wait_tick = value


class ProviderFactory:
    """Factory for AI provider clients."""

    @staticmethod
    def get_client(provider: str = "gemini", settings: Optional[Settings] = None) -> BaseAIClient:
        """
        Get an AI client based on the provider name.
        
        Args:
            provider: 'gemini', 'openai', 'fallback', or 'perplexity'
            settings: Optional application settings
        """
        settings = settings or Settings()
        
        p_lower = provider.lower()
        
        # Fallback client - tries multiple providers
        if p_lower == "fallback" or p_lower == "auto":
            return FallbackClient(settings)
        
        if p_lower == "openai":
            if not settings.openai_api_key:
                logger.warning("OpenAI requested but key is missing, using fallback client")
                return FallbackClient(settings)
            try:
                from ai_service.analyzers.openai_client import OpenAIClient
                return OpenAIClient(settings)
            except Exception as e:
                logger.warning(f"Failed to load OpenAIClient: {e}. Defaulting to Fallback.")
                return FallbackClient(settings)
        
        elif p_lower == "perplexity":
            if not settings.perplexity_api_key:
                logger.warning("Perplexity requested but key is missing, using fallback client")
                return FallbackClient(settings)
            try:
                from ai_service.analyzers.perplexity_client import PerplexityClient
                return PerplexityClient(settings)
            except Exception as e:
                logger.warning(f"Failed to load PerplexityClient: {e}. Defaulting to Fallback.")
                return FallbackClient(settings)
        
        # Default: Use fallback client (Gemini → OpenAI)
        # This ensures we always have a working provider
        return FallbackClient(settings)

    @staticmethod
    def get_best_available_client(settings: Optional[Settings] = None) -> BaseAIClient:
        """Get the best available client with automatic fallback."""
        return FallbackClient(settings or Settings())

    @staticmethod
    def get_cheap_client(settings: Optional[Settings] = None) -> BaseAIClient:
        """
        Get a cheap/fast client for low-priority preprocessing tasks.
        Uses Gemini Flash (fast, cheap) as primary. Falls back to FallbackClient.
        """
        settings = settings or Settings()
        
        # Prefer Gemini Flash for preprocessing (fast, reliable, free tier)
        if settings.gemini_api_key:
            try:
                # Use standard Gemini client, it defaults to gemini-2.0-flash
                logger.info("CheapClient: Using Gemini Flash for preprocessing")
                return GeminiClient(settings)
            except Exception as e:
                logger.warning(f"CheapClient: Gemini failed: {e}")
        
        # Fallback to full FallbackClient if Gemini unavailable
        logger.info("CheapClient: Gemini not available, using FallbackClient")
        return FallbackClient(settings)

