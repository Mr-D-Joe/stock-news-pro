import os
import logging
from fastapi import FastAPI

logger = logging.getLogger(__name__)
from ai_service.analyzers.provider_factory import ProviderFactory
from ai_service.analyzers.impact_analyzer import ImpactAnalyzer
from ai_service.models.article import ArticleCollection, AnalysisResult
from ai_service.processors.browser_extractor import BrowserExtractor
from ai_service.analyzers.essay_generator import EssayGenerator
from ai_service.pipeline.base import PipelineContext, PipelineConfig
from ai_service.health import router as health_router
from ai_service.api.engine import router as engine_router, normalize_language
from ai_service.config import Settings

from ai_service.processors.ticker_resolver import TickerResolver
from ai_service.fetchers.historic_analyzer import HistoricAnalyzer
from ai_service.processors.html_reporter import HtmlReporter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

# --- RESILIENCE: Signal Handling ---
import signal
import sys
import asyncio

def handle_sigint(signum, frame):
    logger.warning("Received SIGINT (Ctrl+C). Forcing clean shutdown...")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_sigint)

signal.signal(signal.SIGINT, handle_sigint)

# --- LIFECYCLE: Database & Resource Management ---
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize Database
    from ai_service.database import init_db
    logger.info("💽 Initializing persistence layer (SQLite)...")
    init_db()
    yield
    # Shutdown: (Optional cleanup)
    logger.info("🛑 Shutting down AI Service...")

app = FastAPI(title="Stock News AI Service", version="1.0.0", lifespan=lifespan)

# --- RESILIENCE: Global Exception Handler ---
from fastapi import Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from ai_service.database import get_session
from ai_service.models import Transaction

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global Crash Handler caught: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "detail": str(exc), "advice": "Please retry. If persistent, check logs."}
    )

# Register routers
app.include_router(health_router)
app.include_router(engine_router)

# Load settings once at startup
_settings = Settings()

# STRICT API GOVERNANCE: Warn if DEV_MODE is off (real APIs will be called)
if _settings.dev_mode:
    logger.info("🔒 DEV_MODE is ON - Using mock data, no external API calls")
else:
    logger.warning("⚠️ DEV_MODE is OFF - Real external APIs will be called (tokens consumed)")

@app.get("/")
async def root():
    providers = _settings.get_available_providers()
    return {
        "status": "AI Service Online", 
        "providers": providers,
        "version": "1.0.0"
    }

@app.get("/resolve/ticker")
async def resolve_ticker(query: str):
    """Resolve fuzzy stock name to ticker."""
    if _settings.dev_mode:
        from ai_service.mock import get_mock_ticker_resolver
        resolver = get_mock_ticker_resolver(_settings)
    else:
        resolver = TickerResolver(_settings)
    return await resolver.resolve_stock(query)

@app.get("/resolve/sector")
async def resolve_sector(query: str):
    """Resolve fuzzy sector name."""
    if _settings.dev_mode:
        from ai_service.mock import get_mock_ticker_resolver
        resolver = get_mock_ticker_resolver(_settings)
    else:
        resolver = TickerResolver(_settings)
    sector = await resolver.resolve_sector(query)
    return {"sector": sector}

@app.get("/api/fundamentals")
async def get_fundamentals(ticker: str):
    """
    Get fundamental data for a stock.
    Returns valuation metrics, analyst targets, and business context.
    Uses mock data in DEV_MODE, real HistoricAnalyzer in production.
    """
    ticker = ticker.upper().strip()
    
    if _settings.dev_mode:
        from ai_service.mock import get_mock_historic_analyzer
        analyzer = get_mock_historic_analyzer(_settings)
        fundamentals = await analyzer.get_fundamentals(ticker)
        
        if not fundamentals:
            return {"error": f"Ticker {ticker} not found in mock data", "found": False}
        
        return {
            "ticker": ticker,
            "found": True,
            "fundamentals": {
                "pe_ratio": fundamentals.get("pe_ratio"),
                "peg_ratio": fundamentals.get("peg_ratio"),
                "roe": fundamentals.get("roe"),
                "debt_to_equity": fundamentals.get("debt_to_equity"),
                "target_mean_price": fundamentals.get("target_mean_price"),
                "target_high_price": fundamentals.get("target_high_price"),
                "target_low_price": fundamentals.get("target_low_price"),
                "recommendation": fundamentals.get("recommendation"),
                "executive_summary": fundamentals.get("executive_summary", ""),
                "business_summary": fundamentals.get("business_summary"),
                "sector": fundamentals.get("sector"),
                "industry": fundamentals.get("industry"),
                "market_cap": fundamentals.get("market_cap"),
                "beta": fundamentals.get("beta"),
                "dividend_yield": fundamentals.get("dividend_yield"),
                "revenue_growth": fundamentals.get("revenue_growth"),
                "profit_margin": fundamentals.get("profit_margin"),
            }
        }
    else:
        # Production: Use real HistoricAnalyzer
        analyzer = HistoricAnalyzer(_settings)
        fundamentals = await analyzer.get_fundamentals(ticker) if hasattr(analyzer.get_fundamentals, '__call__') else analyzer.get_fundamentals(ticker)
        
        if not fundamentals:
            return {"error": f"Could not fetch fundamentals for {ticker}", "found": False}
        
        return {
            "ticker": ticker,
            "found": True,
            "fundamentals": fundamentals
        }

@app.get("/api/price_history")
async def get_price_history(ticker: str, period: str = "1y"):
    """
    Get price history for a stock.
    
    Periods: 24h, 1wk, 1mo, 3mo, 1y, 10y
    For 24h: Returns intraday data (15-min intervals)
    Uses mock data in DEV_MODE.
    """
    ticker = ticker.upper().strip()
    valid_periods = ["24h", "1wk", "1mo", "3mo", "1y", "10y"]
    if period not in valid_periods:
        period = "1y"
    
    if _settings.dev_mode:
        from ai_service.mock.mock_data import get_mock_price_data
        return get_mock_price_data(ticker, period)
    else:
        # Production: Use real data source (to be implemented)
        # For now, return mock data as fallback
        from ai_service.mock.mock_data import get_mock_price_data
        return get_mock_price_data(ticker, period)

@app.get("/api/sector_news")
async def get_sector_news(sector: str):
    """
    Get sector-wide news headlines.
    
    Returns news for the entire sector, not stock-specific.
    Used for the sector news ticker in the GUI.
    """
    if _settings.dev_mode:
        from ai_service.mock.mock_data import get_mock_sector_news
        news = get_mock_sector_news(sector)
        return {
            "sector": sector,
            "news": [
                {
                    "title": item["title"],
                    "source": item["source"],
                    "date": item["published"].strftime("%Y-%m-%d %H:%M"),
                    "summary": item.get("summary", "")
                }
                for item in news
            ]
        }
    else:
        # Production: Use real news fetcher (to be implemented)
        from ai_service.mock.mock_data import get_mock_sector_news
        news = get_mock_sector_news(sector)
        return {
            "sector": sector,
            "news": [
                {
                    "title": item["title"],
                    "source": item["source"],
                    "date": item["published"].strftime("%Y-%m-%d %H:%M"),
                    "summary": item.get("summary", "")
                }
                for item in news
            ]
        }

@app.post("/analyze/essay", response_model=AnalysisResult)
async def analyze_essay(request: ArticleCollection, language: str = "German", use_browser: bool = True):
    """Generate an essay from the provided articles."""
    if use_browser:
        browser = BrowserExtractor()
        request = await browser._process_async(request)

    context = PipelineContext(
        config=PipelineConfig(
            stocks=request.query_stocks,
            sectors=request.query_sectors or ["General"],
            language=normalize_language(language)
        )
    )
    
    generator = EssayGenerator()
    result = generator.process(request, context)
    return result

@app.post("/analyze/full_report")
async def analyze_full_report(request: ArticleCollection, language: str = "German"):
    """
    Generate a full HTML report including historical data, AI analysis, and news markers.
    Fetches news internally if none provided.
    Delegates to WorkflowOrchestrator.
    """
    from ai_service.pipeline.orchestrator import WorkflowOrchestrator
    
    # Normalize language input for fault tolerance
    language = normalize_language(language)
    
    orchestrator = WorkflowOrchestrator(_settings)
    result = await orchestrator.run(request, language)
    
    return result

@app.post("/analyze/theme")
async def analyze_theme(request: dict):
    """
    Analyze a thematic trend (e.g., "AI", "War").
    Returns Winners/Losers and an Essay.
    """
    from ai_service.theme_service import ThemeService
    
    query = request.get("query", "").strip()
    if not query:
        return {"error": "Query parameter is required"}
        
    service = ThemeService()
    service = ThemeService()
    return service.analyze_theme(query)

# --- PORTFOLIO API (Persistence) ---

@app.post("/portfolio/transactions", response_model=Transaction)
async def add_transaction(transaction: Transaction, session: Session = Depends(get_session)):
    """
    Add a new transaction to the portfolio.
    (BE-REQ-PORTFOLIO-02)
    """
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    logger.info(f"💾 Persisted Transaction: {transaction.symbol} x {transaction.amount}")
    return transaction

@app.get("/portfolio/transactions", response_model=list[Transaction])
async def get_transactions(session: Session = Depends(get_session)):
    """
    Get all portfolio transactions.
    (BE-REQ-PORTFOLIO-03)
    """
    statement = select(Transaction).order_by(Transaction.timestamp.desc())
    results = session.exec(statement)
    return results.all()

@app.delete("/portfolio/transactions/{transaction_id}")
async def delete_transaction(transaction_id: int, session: Session = Depends(get_session)):
    """
    Delete a transaction by ID.
    (BE-REQ-PORTFOLIO-04)
    """
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    session.delete(transaction)
    session.commit()
    return {"ok": True}

@app.get("/api/quota")
async def get_quota_status():
    """
    Get rate limit status for all AI providers.
    Shows remaining quota, reset times, and recommended wait times.
    """
    from ai_service.analyzers.gemini_client import GeminiClient
    from datetime import datetime
    
    status = {
        "timestamp": datetime.now().isoformat(),
        "providers": {}
    }
    
    # Gemini Status (uses shared rate limiter)
    try:
        if GeminiClient._rate_limiter:
            gemini_status = GeminiClient._rate_limiter.get_status()
            status["providers"]["gemini"] = {
                "model": _settings.gemini_model,
                "rate_limited": gemini_status.get("rate_limited", False),
                "wait_seconds": gemini_status.get("remaining_seconds", 0),
                "available_at": gemini_status.get("available_at"),
                "limits": {
                    "rpm": 15,
                    "rpd": 1000,
                    "note": "Free Tier - gemini-2.5-flash-lite"
                }
            }
        else:
            status["providers"]["gemini"] = {"status": "not initialized"}
    except Exception as e:
        status["providers"]["gemini"] = {"error": str(e)}
    
    # OpenAI Status
    status["providers"]["openai"] = {
        "model": _settings.openai_model,
        "status": "check OpenAI dashboard for usage",
        "limits": {
            "note": "Tier-based. Free tier very limited (~3 RPM)"
        }
    }
    
    # Groq Status
    status["providers"]["groq"] = {
        "model": _settings.groq_model,
        "limits": {
            "rpm": 30,
            "rpd": 1000,
            "tpm": 12000,
            "tpd": 100000,
            "note": "Free Tier. Check Groq Console for precise limits."
        }
    }
    
    # OpenRouter Status
    status["providers"]["openrouter"] = {
        "model": _settings.openrouter_model,
        "limits": {
            "rpm": 20,
            "rpd": 50,
            "note": "Free users: 50 req/day. $10+ credit: 1000 req/day"
        }
    }
    
    # Recommendation
    gemini_wait = status["providers"].get("gemini", {}).get("wait_seconds", 0)
    if gemini_wait > 0:
        status["recommendation"] = f"Gemini available in {gemini_wait}s. Wait for premium quality."
    elif gemini_wait == 0:
        status["recommendation"] = "Gemini ready. Premium analysis available."
    else:
        status["recommendation"] = "Check individual providers."
    
    return status

