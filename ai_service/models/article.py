from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field

from ai_service.models.impact import ImpactAnalysisResult
from ai_service.models.price_data import PriceHistory

class CalendarEvent(BaseModel):
    title: str
    date: str
    description: str

class Article(BaseModel):
    title: str
    link: str
    source: str
    published: datetime
    summary: Optional[str] = None
    content: Optional[str] = None
    citation_id: Optional[int] = None
    
    def to_citation_reference(self) -> str:
        date_str = self.published.strftime("%Y-%m-%d")
        return f"[{self.citation_id}] {self.source}: {self.title} ({date_str}) - {self.link}"

class ArticleCollection(BaseModel):
    articles: List[Article] = []
    query_stocks: List[str] = []
    query_sectors: List[str] = []
    collected_at: datetime = Field(default_factory=datetime.now)
    
    # Analysis results attached to the collection
    impact_analysis: Optional[ImpactAnalysisResult] = None
    price_history: Optional[PriceHistory] = None
    fundamentals: Optional[Dict] = None

    @property
    def count(self) -> int:
        return len(self.articles)

    def assign_citation_ids(self):
        for i, article in enumerate(self.articles, 1):
            article.citation_id = i

class AnalysisResult(BaseModel):
    essay: str
    summary: Optional[str] = None
    key_findings: List[str] = []
    swot: Dict[str, List[str]] = {}
    watch_items: List[str] = []
    upcoming_events: List[CalendarEvent] = []
    anomalies: List[str] = []
    sentiment: str = "neutral"
    
    article_collection: Optional[ArticleCollection] = None
    impact_analysis: Optional[ImpactAnalysisResult] = None
    price_history: Optional[PriceHistory] = None
    fundamentals: Optional[Dict] = None
    metadata: Optional[Dict] = None

