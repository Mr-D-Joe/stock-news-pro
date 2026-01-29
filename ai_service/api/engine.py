"""API Router for Engine communication.

Provides REST endpoints for the C++ Engine to interact with the AI Service.
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, Literal, List
from datetime import datetime
import logging

from ai_service.analyzers.base_client import AIError
from ai_service.analyzers.essay_generator import EssayGenerator
from ai_service.config import Settings
from ai_service.models.article import (
    Article,
    ArticleCollection
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/engine", tags=["Engine"])


# ==================== Language Normalization ====================

# Mapping of various language names/abbreviations to standardized English names
LANGUAGE_MAP = {
    # Turkish variants
    "turkish": "Turkish", "türkisch": "Turkish", "tuerkisch": "Turkish", "tr": "Turkish",
    "tur": "Turkish", "türkçe": "Turkish", "türk": "Turkish",
    "turkish / türkisch": "Turkish",
    # German variants
    "german": "German", "deutsch": "German", "de": "German", "ger": "German",
    "germanisch": "German", "deu": "German", "german / deutsch": "German",
    # English variants
    "english": "English", "englisch": "English", "en": "English", "eng": "English",
    "english / englisch": "English",
    # French variants
    "french": "French", "français": "French", "francais": "French", "französisch": "French",
    "fr": "French", "fra": "French", "french / français": "French",
    # Spanish variants  
    "spanish": "Spanish", "español": "Spanish", "espanol": "Spanish", "spanisch": "Spanish",
    "es": "Spanish", "spa": "Spanish", "spanish / español": "Spanish",
    # Italian variants
    "italian": "Italian", "italiano": "Italian", "italienisch": "Italian", "it": "Italian",
    "ita": "Italian", "italian / italiano": "Italian",
    # Japanese variants
    "japanese": "Japanese", "japanisch": "Japanese", "日本語": "Japanese", "ja": "Japanese",
    "jpn": "Japanese", "nihongo": "Japanese", "japanese / 日本語": "Japanese",
    # Chinese variants
    "chinese": "Chinese", "chinesisch": "Chinese", "中文": "Chinese", "zh": "Chinese",
    "mandarin": "Chinese", "zho": "Chinese", "chinese / 中文": "Chinese",
    # Portuguese variants
    "portuguese": "Portuguese", "portugiesisch": "Portuguese", "português": "Portuguese",
    "pt": "Portuguese", "por": "Portuguese", "portuguese / português": "Portuguese",
    # Russian variants
    "russian": "Russian", "russisch": "Russian", "русский": "Russian", "ru": "Russian",
    "rus": "Russian", "russian / русский": "Russian",
    # Dutch variants
    "dutch": "Dutch", "niederländisch": "Dutch", "holländisch": "Dutch", "nl": "Dutch",
    "nld": "Dutch", "nederlands": "Dutch", "dutch / nederlands": "Dutch",
    # Korean variants
    "korean": "Korean", "koreanisch": "Korean", "한국어": "Korean", "ko": "Korean",
    "kor": "Korean", "korean / 한국어": "Korean",
    # Arabic variants
    "arabic": "Arabic", "arabisch": "Arabic", "العربية": "Arabic", "ar": "Arabic",
    "ara": "Arabic", "arabic / العربية": "Arabic",
    # Polish variants
    "polish": "Polish", "polnisch": "Polish", "polski": "Polish", "pl": "Polish",
    "pol": "Polish", "polish / polski": "Polish",
}

def normalize_language(lang: str) -> str:
    """Normalize language input with fault tolerance.
    
    Maps various language names, abbreviations, and native names 
    to standardized English language names.
    
    Args:
        lang: Input language string (any format)
        
    Returns:
        Normalized English language name, or original if not found
    """
    if not lang:
        return "German"  # Default
    
    # Try exact match first (case-insensitive)
    normalized = LANGUAGE_MAP.get(lang.lower().strip())
    if normalized:
        return normalized
    
    # If not found, return the original (Gemini might understand it)
    # But capitalize first letter for consistency
    return lang.strip().capitalize()


# ==================== Request/Response Models ====================

class NewsItem(BaseModel):
    """Single news item from RSS or API."""
    ticker: str
    title: str
    source: str
    url: Optional[str] = None
    published: Optional[datetime] = None
    summary: Optional[str] = None
    fetched_at: Optional[datetime] = None  # When we fetched this news
    
    def __init__(self, **data):
        super().__init__(**data)
        if self.fetched_at is None:
            self.fetched_at = datetime.now()


class NewsSubmission(BaseModel):
    """Batch of news items submitted by engine."""
    items: list[NewsItem]
    request_analysis: bool = False


class NewsResponse(BaseModel):
    """Response after processing news items."""
    processed: int
    analysis_triggered: bool = False
    message: str


class FetchRequest(BaseModel):
    """Request to fetch news for tickers."""
    tickers: list[str]
    max_per_ticker: int = 50


class AnalysisRequest(BaseModel):
    """Request for AI analysis."""
    tickers: list[str]
    sectors: Optional[list[str]] = None
    language: str = "German"


class SectorStock(BaseModel):
    """Subset of stock data for sector visualization."""
    symbol: str
    name: str
    performance: float
    market_cap: int


class SectorPerformance(BaseModel):
    """Aggregated performance data for a market sector."""
    id: str
    name: str
    performance: float
    market_cap: int
    top_stocks: list[SectorStock]


class AnalysisMetadata(BaseModel):
    """Metadata about the analysis process."""
    provider: str
    model: str
    duration_seconds: float
    retries: int = 0


class AnalysisResponse(BaseModel):
    """AI analysis response for engine."""
    essay: str
    summary: str
    sentiment: str
    key_findings: list[str]
    generated_at: datetime
    metadata: Optional[AnalysisMetadata] = None


class SparklineResponse(BaseModel):
    """Compact time-series data for sparkline visualization."""
    ticker: str
    period: str
    data: list[float]
    source: str


class ErrorInfo(BaseModel):
    code: str
    message: str


class NewsResponseEnvelope(BaseModel):
    status: Literal["success", "partial", "error"]
    data: Optional[NewsResponse] = None
    error: Optional[ErrorInfo] = None


class AnalysisResponseEnvelope(BaseModel):
    status: Literal["success", "partial", "error"]
    data: Optional[AnalysisResponse] = None
    error: Optional[ErrorInfo] = None


class SectorPerformanceEnvelope(BaseModel):
    status: Literal["success", "partial", "error"]
    data: Optional[List[SectorPerformance]] = None
    error: Optional[ErrorInfo] = None


class SparklineResponseEnvelope(BaseModel):
    status: Literal["success", "partial", "error"]
    data: Optional[SparklineResponse] = None
    error: Optional[ErrorInfo] = None



class DBRecordRequest(BaseModel):
    """Request to store data in Python-side cache."""
    ticker: str
    title: str
    category: Optional[str] = None
    relevance: Optional[float] = None
    date: Optional[str] = None


class DBQueryRequest(BaseModel):
    """Query parameters for DB lookup."""
    ticker: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    limit: int = 100


# ==================== In-Memory Cache ====================
# Simple cache for Engine-submitted data (would be Redis in production)

_news_cache: list[NewsItem] = []
_analysis_cache: dict[str, AnalysisResponse] = {}
_analysis_hash_cache: dict[str, str] = {}  # cache_key -> content_hash


def _compute_news_hash(articles: list) -> str:
    """Compute MD5 hash of news content to detect changes."""
    import hashlib
    content = "".join(sorted([a.title for a in articles]))
    return hashlib.md5(content.encode()).hexdigest()


def _get_fresh_news(ticker: Optional[str] = None, max_age_hours: int = 24) -> list[NewsItem]:
    """Get only fresh news items (within max_age_hours)."""
    from datetime import timedelta
    cutoff = datetime.now() - timedelta(hours=max_age_hours)
    items = _news_cache
    if ticker:
        items = [n for n in items if n.ticker.upper() == ticker.upper()]
    return [n for n in items if n.fetched_at and n.fetched_at >= cutoff]


class RateLimitStatus(BaseModel):
    """Rate limit status response."""
    rate_limited: bool
    remaining_seconds: int
    available_at: Optional[str] = None
    message: str


# ==================== Endpoints ====================

@router.get("/rate-limit")
async def get_rate_limit_status():
    """
    Get current rate limit status from Gemini API.
    
    Returns the time remaining until the rate limit expires.
    GUI can use this to disable buttons and show countdown.
    """
    try:
        from ai_service.analyzers.gemini_client import GeminiClient
        
        # Access the shared rate limiter
        if GeminiClient._rate_limiter:
            status = GeminiClient._rate_limiter.get_status()
            return RateLimitStatus(**status)
        else:
            return RateLimitStatus(
                rate_limited=False,
                remaining_seconds=0,
                available_at=None,
                message="Ready (no rate limiter initialized)"
            )
    except Exception as e:
        logger.error(f"Error getting rate limit status: {e}")
        return RateLimitStatus(
            rate_limited=False,
            remaining_seconds=0,
            available_at=None,
            message=f"Error: {e}"
        )

@router.post("/news", response_model=NewsResponse)
async def submit_news(submission: NewsSubmission):
    """
    Receive news items from C++ Engine.
    
    Engine calls this after fetching from RSS/APIs.
    Optionally triggers AI analysis.
    """
    global _news_cache
    
    # Store in cache
    _news_cache.extend(submission.items)
    
    # Limit cache size
    if len(_news_cache) > 1000:
        _news_cache = _news_cache[-500:]
    
    logger.info(f"Received {len(submission.items)} news items from engine")
    
    analysis_triggered = False
    if submission.request_analysis and len(submission.items) > 0:
        # Would trigger async analysis here
        analysis_triggered = True
        logger.info("Analysis requested - would queue for processing")
    
    return NewsResponse(
        processed=len(submission.items),
        analysis_triggered=analysis_triggered,
        message=f"Successfully processed {len(submission.items)} items"
    )


@router.get("/news")
async def get_cached_news(
    ticker: Optional[str] = Query(None, description="Filter by ticker"),
    limit: int = Query(50, le=200, description="Max items to return")
):
    """
    Retrieve cached news items.
    
    Engine can query back processed news.
    """
    items = _news_cache
    
    if ticker:
        items = [n for n in items if n.ticker.upper() == ticker.upper()]
    
    return {"items": items[-limit:], "total": len(items)}


@router.post("/analyze", response_model=AnalysisResponse)
async def request_analysis(request: AnalysisRequest):
    """
    Request AI analysis for specific tickers.
    
    Engine calls this to get AI-generated insights.
    Uses caching with content hash to avoid redundant AI calls.
    """
    from ai_service.pipeline.base import PipelineContext, PipelineConfig
    
    # Build cache key
    cache_key = f"{'-'.join(sorted(request.tickers))}:{normalize_language(request.language)}"
    
    # Build article collection from cached news
    relevant_news = [
        n for n in _news_cache 
        if n.ticker.upper() in [t.upper() for t in request.tickers]
    ]
    
    # OPTIMIZATION: Check if news content has changed since last analysis
    current_hash = _compute_news_hash(relevant_news) if relevant_news else "empty"
    
    if cache_key in _analysis_cache and cache_key in _analysis_hash_cache:
        if _analysis_hash_cache[cache_key] == current_hash:
            logger.info(f"🔄 Using cached analysis for {cache_key} (content unchanged)")
            return _analysis_cache[cache_key]
    
    if not relevant_news:
        raise HTTPException(
            status_code=404, 
            detail=f"No cached news found for tickers: {request.tickers}"
        )
    
    # Convert to Article objects
    articles = [
        Article(
            title=n.title,
            link=n.url or f"https://news.example.com/{n.ticker}",
            source=n.source,
            published=n.published or datetime.now(),
            summary=n.summary
        )
        for n in relevant_news
    ]
    
    collection = ArticleCollection(
        articles=articles,
        query_stocks=request.tickers,
        query_sectors=request.sectors or []
    )
    collection.assign_citation_ids()
    
    # Generate analysis
    context = PipelineContext(
        config=PipelineConfig(
            stocks=request.tickers,
            sectors=request.sectors or ["General"],
            language=normalize_language(request.language)
        )
    )
    
    generator = EssayGenerator()
    
    try:
        result = generator.process(collection, context)
    except AIError as e:
        error_msg = str(e)
        logger.warning(f"Analysis failed with AIError: {error_msg}")
        if "rate limit" in error_msg.lower() or "quota" in error_msg.lower():
            raise HTTPException(status_code=429, detail=f"Rate limit exceeded: {error_msg}")
        raise HTTPException(status_code=503, detail=f"AI Service unavailable: {error_msg}")
    except Exception as e:
        logger.error(f"Analysis generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {e}")
    
    # Construct proper AnalysisMetadata from result
    meta = result.metadata or {}
    analysis_meta = AnalysisMetadata(
        provider=meta.get('provider', 'unknown'),
        model=meta.get('model', 'unknown'),
        duration_seconds=meta.get('duration_seconds', 0.0),
        retries=meta.get('retries', 0)
    )
    
    response = AnalysisResponse(
        essay=result.essay,
        summary=result.summary or "",
        sentiment=result.sentiment,
        key_findings=result.key_findings,
        generated_at=datetime.now(),
        metadata=analysis_meta
    )
    
    # Cache the analysis with content hash
    _analysis_cache[cache_key] = response
    _analysis_hash_cache[cache_key] = current_hash
    logger.info(f"💾 Cached analysis for {cache_key} (hash: {current_hash[:8]}...)")
    
    return response


@router.get("/analyze/{ticker}")
async def get_cached_analysis(ticker: str):
    """
    Get cached analysis for a ticker.
    
    Avoids re-running expensive AI calls.
    """
    # Check single ticker cache
    if ticker.upper() in _analysis_cache:
        return _analysis_cache[ticker.upper()]
    
    # Check if part of any cached analysis
    for key, analysis in _analysis_cache.items():
        if ticker.upper() in key.upper():
            return analysis
    
    raise HTTPException(status_code=404, detail=f"No cached analysis for: {ticker}")


@router.post("/db/store")
async def store_record(record: DBRecordRequest):
    """
    Store a record (engine can persist via Python).
    
    Alternative to direct SQLite access from C++.
    """
    # In production, this would write to a real database
    logger.info(f"Storing record for ticker: {record.ticker}")
    return {"stored": True, "ticker": record.ticker}


@router.delete("/cache")
async def clear_cache():
    """Clear all caches (for testing/maintenance)."""
    global _news_cache, _analysis_cache, _analysis_hash_cache
    _news_cache = []
    _analysis_cache = {}
    _analysis_hash_cache = {}
    logger.info("🗑️ All caches cleared")
    return {"cleared": True}


@router.post("/fetch")
async def fetch_news(request: FetchRequest):
    """
    Fetch news from external sources for given tickers.
    
    Fetches from:
    - yfinance (stock-specific news)
    - Google Finance RSS
    - Yahoo Finance RSS
    
    Returns fetched items and adds them to cache.
    """
    global _news_cache
    
    try:
        from ai_service.fetchers import get_fetcher
        
        fetcher = get_fetcher()
        news_items = await fetcher.fetch_multiple_tickers(
            request.tickers, 
            max_per_ticker=request.max_per_ticker
        )
        
        # Convert to NewsItem and add to cache
        for item in news_items:
            news_item = NewsItem(
                ticker=item.ticker,
                title=item.title,
                source=item.source,
                url=item.url,
                published=item.published,
                summary=item.summary
            )
            _news_cache.append(news_item)
        
        # Limit cache size
        if len(_news_cache) > 1000:
            _news_cache = _news_cache[-500:]
        
        logger.info(f"Fetched {len(news_items)} news items for {request.tickers}")
        
        return {
            "fetched": len(news_items),
            "tickers": request.tickers,
            "items": [
                {
                    "ticker": item.ticker,
                    "title": item.title,
                    "source": item.source,
                    "url": item.url,
                    "published": item.published.isoformat() if item.published else None
                }
                for item in news_items  # Return all items
            ]
        }
        
    except ImportError as e:
        logger.error(f"Fetcher import failed: {e}")
        raise HTTPException(
            status_code=500, 
            detail="News fetcher not available. Install: pip install yfinance feedparser"
        )
    except Exception as e:
        logger.error(f"Fetch failed: {e}")
        raise HTTPException(status_code=500, detail=f"Fetch failed: {e}")


@router.get("/sectors/performance", response_model=list[SectorPerformance])
async def get_sectors(
    period: str = Query("1d", description="Time period for performance (1d, 1w, 1m, 1y)")
):
    """
    Get market sector performance.
    
    Implements BE-REQ-SECTOR-01 to BE-REQ-SECTOR-04.
    In DEV_MODE, returns rich mock data.
    """
    from ai_service.mock.mock_data import get_mock_sector_performance
    
    settings = Settings()
    
    data = get_mock_sector_performance(period)
    if settings.dev_mode:
        return [SectorPerformance(**s) for s in data]
    
    # In Real mode, this would fetch from a real provider (e.g. FMP)
    # For now, return mock even in real mode but with a warning in logs
    return [SectorPerformance(**s) for s in data]


@router.get("/stocks/{ticker}/sparkline", response_model=SparklineResponse)
async def get_sparkline(
    ticker: str,
    period: str = Query("1w", description="Time period (1d, 1w, 1m)")
):
    """
    Get compact sparkline data for a ticker.
    
    Implements BE-REQ-SPARK-01 and BE-REQ-SPARK-02.
    """
    from ai_service.mock.mock_data import get_mock_sparkline_data
    
    settings = Settings()
    
    # Unified source identification
    source = "mock" if settings.dev_mode else "real-fallback-mock"
    
    if not settings.dev_mode:
        logger.warning(f"Real sparkline data for {ticker} not available - falling back to mock")
    
    data = get_mock_sparkline_data(ticker, period)
    
    return SparklineResponse(
        ticker=ticker.upper(),
        period=period,
        data=data,
        source=source
    )


# ==================== Versioned API (v1) ====================

@router.post("/v1/news", response_model=NewsResponseEnvelope)
async def submit_news_v1(submission: NewsSubmission):
    try:
        data = await submit_news(submission)
        return NewsResponseEnvelope(status="success", data=data)
    except HTTPException as exc:
        return NewsResponseEnvelope(status="error", error=ErrorInfo(code=str(exc.status_code), message=str(exc.detail)))
    except Exception as exc:
        return NewsResponseEnvelope(status="error", error=ErrorInfo(code="500", message=str(exc)))


@router.post("/v1/analyze", response_model=AnalysisResponseEnvelope)
async def request_analysis_v1(request: AnalysisRequest):
    try:
        data = await request_analysis(request)
        return AnalysisResponseEnvelope(status="success", data=data)
    except HTTPException as exc:
        return AnalysisResponseEnvelope(status="error", error=ErrorInfo(code=str(exc.status_code), message=str(exc.detail)))
    except Exception as exc:
        return AnalysisResponseEnvelope(status="error", error=ErrorInfo(code="500", message=str(exc)))


@router.get("/v1/sectors/performance", response_model=SectorPerformanceEnvelope)
async def get_sectors_v1(
    period: str = Query("1d", description="Time period for performance (1d, 1w, 1m, 1y)")
):
    try:
        data = await get_sectors(period)
        return SectorPerformanceEnvelope(status="success", data=data)
    except HTTPException as exc:
        return SectorPerformanceEnvelope(status="error", error=ErrorInfo(code=str(exc.status_code), message=str(exc.detail)))
    except Exception as exc:
        return SectorPerformanceEnvelope(status="error", error=ErrorInfo(code="500", message=str(exc)))


@router.get("/v1/stocks/{ticker}/sparkline", response_model=SparklineResponseEnvelope)
async def get_sparkline_v1(
    ticker: str,
    period: str = Query("1w", description="Time period (1d, 1w, 1m)")
):
    try:
        data = await get_sparkline(ticker, period)
        return SparklineResponseEnvelope(status="success", data=data)
    except HTTPException as exc:
        return SparklineResponseEnvelope(status="error", error=ErrorInfo(code=str(exc.status_code), message=str(exc.detail)))
    except Exception as exc:
        return SparklineResponseEnvelope(status="error", error=ErrorInfo(code="500", message=str(exc)))
