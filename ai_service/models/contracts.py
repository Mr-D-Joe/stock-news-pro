"""Data contracts for clean module-to-module data transfer.

These TypedDicts define the structure of data passed between components,
ensuring consistency between mock and real implementations.
"""

from typing import TypedDict, Optional, List, Dict
from datetime import datetime


class FundamentalsData(TypedDict, total=False):
    """Fundamental stock metrics."""
    pe_ratio: Optional[float]
    peg_ratio: Optional[float]
    roe: Optional[float]
    debt_to_equity: Optional[float]
    target_mean_price: Optional[float]
    target_high_price: Optional[float]
    target_low_price: Optional[float]
    recommendation: Optional[str]
    business_summary: Optional[str]
    sector: Optional[str]
    industry: Optional[str]
    market_cap: Optional[int]
    beta: Optional[float]
    dividend_yield: Optional[float]
    revenue_growth: Optional[float]
    profit_margin: Optional[float]


class PriceDataPoint(TypedDict):
    """Single price data point."""
    date: str
    close: float
    open: Optional[float]
    high: Optional[float]
    low: Optional[float]
    volume: Optional[int]


class PriceHistory(TypedDict):
    """Historical price data for a period."""
    ticker: str
    period: str
    data: List[PriceDataPoint]
    last_price: float
    source: str


class NewsItem(TypedDict, total=False):
    """News article data."""
    title: str
    source: str
    published: Optional[datetime]
    summary: Optional[str]
    url: Optional[str]
    ticker: Optional[str]


class DeepWebSource(TypedDict, total=False):
    """Deep web research source."""
    title: str
    url: str
    summary: str
    source: str
    published: Optional[datetime]


class EventItem(TypedDict, total=False):
    """Stock-moving event."""
    title: str
    date: str
    category: str
    impact: str  # high, medium, low
    summary: str
    source: Optional[str]
    url: Optional[str]


class SWOTAnalysis(TypedDict):
    """SWOT analysis structure."""
    strengths: List[str]
    weaknesses: List[str]
    opportunities: List[str]
    threats: List[str]


class AnalysisOutput(TypedDict, total=False):
    """AI analysis output structure."""
    essay: str
    summary: str
    swot: SWOTAnalysis
    key_findings: List[str]
    watch_items: List[str]
    buffett_view: str
    lynch_view: str
    outlook: str


class StockResolution(TypedDict, total=False):
    """Stock ticker resolution result."""
    symbol: str
    name: str
    sector: str
    found: bool


class ReportData(TypedDict, total=False):
    """Complete data for HTML report generation."""
    ticker: str
    company_name: str
    sector: str
    business_context: str
    analysis: AnalysisOutput
    price_data: Dict[str, PriceHistory]
    historic_events: List[EventItem]
    fundamentals: FundamentalsData
    last_price: float
    news_count: int


class PipelineResult(TypedDict, total=False):
    """Result from WorkflowOrchestrator.run()."""
    status: str
    dev_mode: bool
    report_path: str
    ticker: str
    company_name: str
    news_analyzed: int
    items: List[EventItem]
