"""Secure API key management utilities.

Best practices for Bearer token authentication:
1. Store keys in environment variables or .env file (never in code)
2. Use HTTPS for all API calls (Bearer tokens are vulnerable over HTTP)
3. Validate key format before use
4. Mask keys in logs
5. Check for key expiration/rotation
"""

import re
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)


class SecureKeyManager:
    """Manages API keys securely with validation and masking."""
    
    # Key format patterns for validation
    KEY_PATTERNS = {
        "gemini": r"^AIza[a-zA-Z0-9_-]{35}$",  # Google API key format
        "openai": r"^sk-[a-zA-Z0-9]{48,}$",    # OpenAI key format  
        "groq": r"^gsk_[a-zA-Z0-9]{52}$",      # Groq key format
        "perplexity": r"^pplx-[a-zA-Z0-9]{48}$",  # Perplexity format
        "huggingface": r"^hf_[a-zA-Z0-9]{34}$",   # HuggingFace format
        "finnhub": r"^[a-z0-9]{20}$",          # Finnhub format
        "fmp": r"^[a-zA-Z0-9]{32}$",           # FMP format
    }
    
    @classmethod
    def mask_key(cls, key: str, show_chars: int = 4) -> str:
        """Mask API key for safe logging.
        
        Args:
            key: The API key to mask
            show_chars: Number of characters to show at start/end
            
        Returns:
            Masked key like "sk-ab...xy"
        """
        if not key or len(key) < show_chars * 2 + 3:
            return "***"
        return f"{key[:show_chars]}...{key[-show_chars:]}"
    
    @classmethod
    def validate_key_format(cls, key: str, provider: str) -> bool:
        """Validate API key format for a provider.
        
        Args:
            key: The API key to validate
            provider: Provider name (gemini, openai, etc.)
            
        Returns:
            True if key format is valid
        """
        if not key:
            return False
            
        pattern = cls.KEY_PATTERNS.get(provider.lower())
        if pattern:
            return bool(re.match(pattern, key))
        
        # Unknown provider - just check it's not empty
        return len(key) >= 10
    
    @classmethod
    def check_key_present(cls, key: str, provider: str) -> dict:
        """Check if key is present and valid.
        
        Args:
            key: The API key
            provider: Provider name
            
        Returns:
            Dict with status, masked_key, and any warnings
        """
        if not key:
            return {
                "present": False,
                "valid_format": False,
                "masked_key": None,
                "warning": f"{provider} API key not configured"
            }
        
        valid_format = cls.validate_key_format(key, provider)
        
        return {
            "present": True,
            "valid_format": valid_format,
            "masked_key": cls.mask_key(key),
            "warning": None if valid_format else f"{provider} key format looks unusual"
        }
    
    @classmethod
    def get_authorization_header(cls, key: str, auth_type: str = "Bearer") -> dict:
        """Create secure Authorization header.
        
        Args:
            key: The API key
            auth_type: Authentication type (Bearer, Basic, X-API-Key)
            
        Returns:
            Dict with Authorization header
        """
        if auth_type.lower() == "bearer":
            return {"Authorization": f"Bearer {key}"}
        elif auth_type.lower() == "basic":
            import base64
            encoded = base64.b64encode(key.encode()).decode()
            return {"Authorization": f"Basic {encoded}"}
        elif auth_type.lower() == "x-api-key":
            return {"X-API-Key": key}
        else:
            return {"Authorization": f"{auth_type} {key}"}
    
    @classmethod
    def log_key_usage(cls, provider: str, key: str, operation: str = "API call") -> None:
        """Log API key usage with masking.
        
        Args:
            provider: Provider name
            key: The API key (will be masked)
            operation: What operation is being performed
        """
        masked = cls.mask_key(key)
        logger.debug(f"{provider} {operation} using key: {masked}")


@lru_cache(maxsize=1)
def get_key_manager() -> SecureKeyManager:
    """Get singleton key manager instance."""
    return SecureKeyManager()


def check_all_keys_status(settings) -> dict:
    """Check status of all configured API keys.
    
    Args:
        settings: Settings instance with API keys
        
    Returns:
        Dict mapping provider -> key status
    """
    manager = get_key_manager()
    
    return {
        "gemini": manager.check_key_present(settings.gemini_api_key, "gemini"),
        "openai": manager.check_key_present(settings.openai_api_key, "openai"),
        "perplexity": manager.check_key_present(settings.perplexity_api_key, "perplexity"),
        "groq": manager.check_key_present(settings.groq_api_key, "groq"),
        "huggingface": manager.check_key_present(settings.huggingface_api_key, "huggingface"),
        "openrouter": manager.check_key_present(settings.openrouter_api_key, "openrouter"),
        "fmp": manager.check_key_present(settings.fmp_api_key, "fmp"),
        "finnhub": manager.check_key_present(settings.finnhub_api_key, "finnhub"),
    }
