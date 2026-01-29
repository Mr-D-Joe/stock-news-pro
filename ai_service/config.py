from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    """Application configuration with enhanced validation and fallback support."""
    
    # API Keys - Primary Providers
    gemini_api_key: str = Field("", validation_alias="GEMINI_API_KEY")
    openai_api_key: str = Field("", validation_alias="OPENAI_API_KEY")
    perplexity_api_key: str = Field("", validation_alias="PERPLEXITY_API_KEY")
    
    # API Keys - Free/Alternative Providers
    groq_api_key: str = Field("", validation_alias="GROQ_API_KEY")
    huggingface_api_key: str = Field("", validation_alias="HUGGINGFACE_API_KEY")
    
    # API Keys - Data Providers (for fundamentals fallback)
    fmp_api_key: str = Field("", validation_alias="FMP_API_KEY")  # Financial Modeling Prep
    finnhub_api_key: str = Field("", validation_alias="FINNHUB_API_KEY")

    # Gemini Model Configuration
    gemini_model: str = Field("gemini-2.0-flash", validation_alias="GEMINI_MODEL")
    gemini_summary_model: str = Field("gemini-2.0-flash", validation_alias="GEMINI_SUMMARY_MODEL")
    gemini_fallback_model: str = Field("gemini-2.0-flash", validation_alias="GEMINI_FALLBACK_MODEL")
    
    # OpenAI Model Configuration
    openai_model: str = Field("gpt-4o-mini", validation_alias="OPENAI_MODEL")
    
    # Perplexity Model Configuration
    perplexity_model: str = Field("llama-3.1-sonar-small-128k-online", validation_alias="PERPLEXITY_MODEL")
    
    # Groq Model Configuration
    groq_model: str = Field("llama-3.1-70b-versatile", validation_alias="GROQ_MODEL")
    
    # OpenRouter Configuration
    openrouter_api_key: str = Field("", validation_alias="OPENROUTER_API_KEY")
    openrouter_model: str = Field("mistralai/mistral-7b-instruct:free", validation_alias="OPENROUTER_MODEL") # Verified free tier
    
    # Ollama Configuration (Local)
    ollama_base_url: str = Field("http://localhost:11434", validation_alias="OLLAMA_BASE_URL")
    ollama_model: str = Field("llama3.1", validation_alias="OLLAMA_MODEL")
    
    # Timeout & Retry Configuration
    request_timeout_seconds: int = Field(120, validation_alias="REQUEST_TIMEOUT_SECONDS")
    max_retries: int = Field(5, validation_alias="MAX_RETRIES")
    rate_limit_requests_per_minute: int = Field(5, validation_alias="RATE_LIMIT_RPM")
    
    # Rate Limit Thresholds
    rate_limit_wait_threshold_seconds: int = Field(600, validation_alias="RATE_LIMIT_WAIT_THRESHOLD")
    rate_limit_cumulative_threshold_seconds: int = Field(300, validation_alias="RATE_LIMIT_CUMULATIVE_THRESHOLD")
    
    # Service Configuration
    default_language: str = Field("German", validation_alias="DEFAULT_LANGUAGE")
    max_articles_for_ai: int = Field(20, validation_alias="MAX_ARTICLES_FOR_AI")
    
    # Feature Flags
    enable_browser_extraction: bool = Field(True, validation_alias="ENABLE_BROWSER_EXTRACTION")
    enable_anomaly_detection: bool = Field(False, validation_alias="ENABLE_ANOMALY_DETECTION")
    
    # Development Mode - uses mock data, no external API calls
    # SAFE DEFAULT: True prevents accidental API consumption when .env is missing
    dev_mode: bool = Field(True, validation_alias="DEV_MODE")
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    
    def get_available_providers(self) -> list[str]:
        """Return list of configured AI providers."""
        providers = []
        if self.gemini_api_key:
            providers.append("gemini")
        if self.openai_api_key:
            providers.append("openai")
        if self.groq_api_key:
            providers.append("groq")
        if self.huggingface_api_key:
            providers.append("huggingface")
        if self.perplexity_api_key:
            providers.append("perplexity")
        # Ollama doesn't need API key - always available if running
        providers.append("ollama")
        return providers
    
    def has_provider(self, provider: str) -> bool:
        """Check if a specific provider is configured."""
        return provider in self.get_available_providers()
