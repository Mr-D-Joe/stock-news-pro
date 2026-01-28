export interface TopBarProps {
    ticker: string;
    sector: string;
    language: string;
    onAction: (action: string, payload?: any) => void;
}

export interface Metric {
    label: string;
    value: number | string;
    trend?: 'up' | 'down' | 'neutral';
}

export interface ReviewData {
    peRatio: number;
    pegRatio: number;
    roe: number;
    debtToEquity: number;
}

export interface AnalystRatings {
    mean: number;
    high: number;
    low: number;
    recommendation: string;
}

export type Timeframe = '24H' | '7D' | '1M' | '3M' | '6M' | '1Y' | '3Y' | '5Y' | '10Y' | 'ALL';
export type AnalysisScope = 'Stock' | 'Sector' | 'Market' | 'Combined';

export interface RiskAssessment {
    level: 'Low' | 'Medium' | 'High';
    description: string;
}

export interface MarketSentiment {
    trend: 'Bullish' | 'Bearish' | 'Neutral';
    score: number; // 0-100
}

export interface Report {
    stock: string;
    summary: string;
    deepAnalysis: string;
    reviewData: ReviewData;
    analystRatings: AnalystRatings;
    riskAssessment: RiskAssessment; // [NEW]
    marketSentiment: MarketSentiment; // [NEW]
    businessContext: string;
    generatedAt: string; // [NEW] ISO Timestamp
}

export interface Stock {
    symbol: string;
    name: string;
    sector: string;
    price: number;
    change: number;
    history: number[];
}

export interface NewsItem {
    title: string;
    sector: string;
    source: string;
    timestamp: string;
}

export interface Essay {
    stock: string;
    text: string;
}

export interface ChartPoint {
    date: string;
    value: number;
    volume?: number; // [NEW]
}

export interface AnalysisResult {
    report: Report;
    stockNews: NewsItem[]; // [NEW] Separate Ticker 1
    sectorNews: NewsItem[]; // [NEW] Separate Ticker 2
    essay: string;
    chartData: ChartPoint[];
    volumeData?: ChartPoint[]; // [NEW] 48h hourly
}

export interface AppState {
    selectedStock: string;
    selectedSector: string;
    selectedLanguage: string; // New: Language Support
    selectedTimeframe: Timeframe; // [NEW]
    selectedScope: AnalysisScope; // [NEW]
    analysisStatus: 'idle' | 'loading' | 'success' | 'error';
    analysisResult: AnalysisResult | null;
    stocks: Stock[];
}

// Props Interfaces
export interface TopBarProps { }
export interface StatusBarProps {
    statusMessage: string;
    versionInfo: string;
}
export interface EventMonitorCardProps {
    chartData: ChartPoint[];
    volumeData?: ChartPoint[]; // [NEW]
    selectedPeriod: string;
    sectorNews: string[];
}

export interface SectorStock {
    symbol: string;
    name: string;
    performance: number;
    market_cap: number;
}

export interface SectorPerformance {
    id: string;
    name: string;
    performance: number;
    market_cap: number;
    top_stocks: SectorStock[];
}

export interface SparklineResponse {
    ticker: string;
    period: string;
    data: number[];
    source: string;
}


