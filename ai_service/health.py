"""Health check endpoints for monitoring AI service status."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging

from ai_service.config import Settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health", tags=["Health"])


class ProviderStatus(BaseModel):
    """Status of a single AI provider."""
    name: str
    configured: bool
    model: Optional[str] = None
    fallback_model: Optional[str] = None


class HealthResponse(BaseModel):
    """Overall health check response."""
    status: str  # "healthy", "degraded", "unhealthy"
    version: str
    providers: list[ProviderStatus]
    configured_count: int
    default_language: str
    features: dict[str, bool]


class LivenessResponse(BaseModel):
    """Simple liveness probe response."""
    alive: bool


class ReadinessResponse(BaseModel):
    """Readiness probe response."""
    ready: bool
    reason: Optional[str] = None


@router.get("/", response_model=HealthResponse)
async def health_check():
    """
    Comprehensive health check endpoint.
    Returns status of all configured providers and features.
    """
    settings = Settings()
    providers = []
    
    # Check Gemini
    providers.append(ProviderStatus(
        name="gemini",
        configured=bool(settings.gemini_api_key),
        model=settings.gemini_model if settings.gemini_api_key else None,
        fallback_model=settings.gemini_fallback_model if settings.gemini_api_key else None,
    ))
    
    # Check OpenAI
    providers.append(ProviderStatus(
        name="openai",
        configured=bool(settings.openai_api_key),
        model=settings.openai_model if settings.openai_api_key else None,
    ))
    
    # Check Perplexity
    providers.append(ProviderStatus(
        name="perplexity",
        configured=bool(settings.perplexity_api_key),
        model=settings.perplexity_model if settings.perplexity_api_key else None,
    ))
    
    configured_count = sum(1 for p in providers if p.configured)
    
    # Determine overall status
    if configured_count == 0:
        status = "unhealthy"
    elif configured_count < len(providers):
        status = "degraded"
    else:
        status = "healthy"
    
    return HealthResponse(
        status=status,
        version="1.0.0",
        providers=providers,
        configured_count=configured_count,
        default_language=settings.default_language,
        features={
            "browser_extraction": settings.enable_browser_extraction,
            "anomaly_detection": settings.enable_anomaly_detection,
        }
    )


@router.get("/live", response_model=LivenessResponse)
async def liveness_probe():
    """
    Kubernetes-style liveness probe.
    Returns true if the service is running.
    """
    return LivenessResponse(alive=True)


@router.get("/ready", response_model=ReadinessResponse)
async def readiness_probe():
    """
    Kubernetes-style readiness probe.
    Returns true if the service is ready to accept requests.
    """
    settings = Settings()
    providers = settings.get_available_providers()
    
    if not providers:
        return ReadinessResponse(
            ready=False,
            reason="No AI providers configured. Set at least one API key."
        )
    
    return ReadinessResponse(ready=True)


@router.get("/providers/{provider_name}")
async def check_provider(provider_name: str):
    """
    Check if a specific provider is available.
    Does not make actual API calls - just checks configuration.
    """
    settings = Settings()
    
    if provider_name not in ["gemini", "openai", "perplexity"]:
        raise HTTPException(status_code=404, detail=f"Unknown provider: {provider_name}")
    
    if settings.has_provider(provider_name):
        return {"provider": provider_name, "status": "configured"}
    else:
        return {"provider": provider_name, "status": "not_configured"}
