
import logging
from typing import Optional, Callable
from ai_service.config import Settings
from ai_service.analyzers.base_client import BaseAIClient, AIError

logger = logging.getLogger(__name__)

class OpenRouterClient(BaseAIClient):
    """
    Client for OpenRouter API (Access to DeepSeek, Gemma, Llama, etc.).
    Uses OpenAI SDK interface.
    """

    # Fallback models (verified working Jan 2026)
    MODEL_FALLBACK_CHAIN = [
        "meta-llama/llama-3.3-70b-instruct:free",   # Primary - GPT-4 level
        "google/gemma-3-27b-it:free",               # Secondary - Google's multimodal
        "meta-llama/llama-3.1-405b-instruct:free",  # Tertiary - largest open model
    ]

    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        self.api_key = self.settings.openrouter_api_key
        # Use first model in chain as default (verified working)
        self.default_model = self.settings.openrouter_model or "mistralai/mistral-7b-instruct:free"
        
        if not self.api_key:
            raise AIError("OPENROUTER_API_KEY is required")

        try:
            from openai import OpenAI
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.api_key,
                timeout=120.0 # Enforce 2 minute timeout
            )
        except ImportError:
            raise AIError("OpenAI package required for OpenRouter (pip install openai)")

    def generate(self, prompt: str, system_instruction: Optional[str] = None, **kwargs) -> str:
        """Generate content with fallback support."""
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        
        messages.append({"role": "user", "content": prompt})
        
        # Start with default/configured model, then try fallback chain
        models_to_try = [self.default_model] + [
            m for m in self.MODEL_FALLBACK_CHAIN if m != self.default_model
        ]
        
        last_error = None

        for model_name in models_to_try:
            try:
                logger.info(f"Generating with OpenRouter model: {model_name}")
                completion = self.client.chat.completions.create(
                    extra_headers={
                        "HTTP-Referer": "https://stock-news-pro.com",
                        "X-Title": "Stock News Pro",
                    },
                    model=model_name,
                    messages=messages,
                    temperature=kwargs.get("temperature", 0.7),
                    max_tokens=kwargs.get("max_output_tokens", 4096)
                )
                
                return completion.choices[0].message.content
                
            except Exception as e:
                last_error = e
                error_str = str(e).lower()
                
                # If model is not found (404) or unavailable, try next
                if "404" in error_str or "not found" in error_str or "unavailable" in error_str:
                    logger.warning(f"OpenRouter model {model_name} unavailable: {e}. Trying next...")
                    continue
                
                # Rate limits
                if "429" in error_str or "rate limit" in error_str:
                    logger.warning(f"OpenRouter model {model_name} rate limited. Trying next...")
                    continue
                
                # Other errors - log and try next just in case
                logger.warning(f"OpenRouter model {model_name} failed: {e}. Trying next...")
                continue

        logger.error(f"OpenRouter generation failed on all models. Last error: {last_error}")
        raise AIError(f"OpenRouter error: {last_error}")

    def summarize_article(self, title: str, text: str, max_words: int = 100) -> str:
        """Summarize article using OpenRouter."""
        prompt = f"""
        Summarize the following article in approximately {max_words} words.
        Focus on key facts, financial figures, and direct impact.
        
        Title: {title}
        Text:
        {text[:15000]}
        """
        return self.generate(prompt, temperature=0.3)

    def analyze_text(self, text: str, task: str = "summarize", max_words: int = 150) -> str:
        """Analyze/summarize text for Deep Web content processing."""
        if task == "summarize":
            prompt = f"""Summarize this text concisely in about {max_words} words, focusing on financial/investment insights:

{text[:15000]}"""
        else:
            prompt = f"""Analyze the following text and provide key insights:

{text[:15000]}"""
        
        try:
            return self.generate(prompt, temperature=0.3)
        except Exception as e:
            logger.warning(f"OpenRouter analyze_text failed: {e}")
            return ""

    @property
    def on_wait_start(self) -> Optional[Callable[[int, bool], None]]:
        return None

    @on_wait_start.setter
    def on_wait_start(self, value: Optional[Callable[[int, bool], None]]) -> None:
        pass

    @property
    def on_wait_tick(self) -> Optional[Callable[[int], None]]:
        return None

    @on_wait_tick.setter
    def on_wait_tick(self, value: Optional[Callable[[int], None]]) -> None:
        pass
