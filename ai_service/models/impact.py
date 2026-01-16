from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime
from pydantic import BaseModel

class NewsCategory(str, Enum):
    FDA_APPROVAL = "FDA_APPROVAL"
    FDA_REJECTION = "FDA_REJECTION"
    EARNINGS = "EARNINGS"
    PARTNERSHIP = "PARTNERSHIP"
    ACQUISITION = "ACQUISITION"
    ANALYST_RATING = "ANALYST_RATING"
    PRODUCT_LAUNCH = "PRODUCT_LAUNCH"
    CLINICAL_TRIAL = "CLINICAL_TRIAL"
    REGULATORY = "REGULATORY"
    EXECUTIVE = "EXECUTIVE"
    GENERAL_NEWS = "GENERAL_NEWS"
    RUMOR = "RUMOR"

class StockSensitivity(BaseModel):
    symbol: str = "UNKNOWN"
    avg_daily_move_pct: float = 0.0
    volatility_high_events: List[datetime] = []
    sensitivity_score: float = 0.5

class ArticleImpact(BaseModel):
    article_title: str
    article_link: str
    published: Optional[datetime] = None
    category: NewsCategory
    base_weight: float = 1.0
    impact_score: float = 0.0
    relevance_explanation: Optional[str] = None
    relevance_score: float = 0.0
    price_before: Optional[float] = None
    price_after: Optional[float] = None
    price_change_pct: Optional[float] = None

class FundamentalData(BaseModel):
    market_cap: float = 0.0
    pe_ratio: float = 0.0
    sector: str = ""

class ImpactAnalysisResult(BaseModel):
    symbol: str
    articles_analyzed: int = 0
    article_impacts: List[ArticleImpact] = []
    avg_impact_score: float = 0.0
    high_impact_count: int = 0
    category_breakdown: Dict[str, int] = {}
    
    sensitivity_profile: Optional[StockSensitivity] = None
    fundamental_impact: Optional[FundamentalData] = None
