/**
 * RealApiService - HTTP Client for ai_service Backend
 * 
 * Connects to the Python FastAPI backend for real data and AI analysis.
 * Used when VITE_USE_REAL_API=true
 */

import type { Stock, NewsItem, Report, AnalysisResult, ChartPoint, SectorPerformance, SparklineResponse, ThemeResult } from '../types';
import { sanitizeText, buildSanitizationTrace } from './sanitization';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// ==================== Helper Functions ====================

async function fetchJSON<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const response = await fetch(`${API_BASE}${endpoint}`, {
        headers: {
            'Content-Type': 'application/json',
            ...options?.headers,
        },
        ...options,
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: response.statusText }));
        throw new Error(error.detail || `API Error: ${response.status}`);
    }

    return response.json();
}

type ApiEnvelope<T> = {
    status: 'success' | 'partial' | 'error';
    data?: T;
    error?: { code: string; message: string };
};

async function fetchEnvelope<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const response = await fetchJSON<ApiEnvelope<T>>(endpoint, options);
    if (response.status !== 'success' || !response.data) {
        const message = response.error?.message || 'Unknown API error';
        throw new Error(message);
    }
    return response.data;
}

// ==================== Type Mappings ====================

interface BackendTickerResponse {
    symbol: string;
    name: string;
    sector: string;
    exchange?: string;
}

interface BackendAnalysisResponse {
    essay: string;
    summary: string;
    sentiment: string;
    key_findings: string[];
    generated_at: string;
    metadata?: {
        provider: string;
        model: string;
        duration_seconds: number;
    };
}

interface BackendNewsItem {
    title: string;
    source: string;
    date: string;
    summary?: string;
}

// ==================== Service Implementation ====================

export const RealApiService = {
    /**
     * Search for a stock by name or symbol (fuzzy matching)
     */
    searchStock: async (query: string): Promise<Stock | null> => {
        try {
            const result = await fetchJSON<BackendTickerResponse>(
                `/resolve/ticker?query=${encodeURIComponent(query)}`
            );

            if (!result.symbol) return null;

            // Fetch price data for the resolved ticker
            const priceData = await fetchJSON<{
                ticker: string;
                data: { date: string; close: number }[];
                last_price: number;
            }>(`/api/price_history?ticker=${result.symbol}&period=1y`);

            return {
                symbol: result.symbol,
                name: result.name,
                sector: result.sector || 'General',
                price: priceData.last_price || 0,
                change: 0, // Would need additional API for daily change
                history: priceData.data?.map(d => d.close) || [],
            };
        } catch (error) {
            console.error('RealApiService.searchStock error:', error);
            return null;
        }
    },

    /**
     * Get sector news
     */
    getSectorNews: async (sector: string): Promise<NewsItem[]> => {
        try {
            const result = await fetchJSON<{ sector: string; news: BackendNewsItem[] }>(
                `/api/sector_news?sector=${encodeURIComponent(sector)}`
            );

            return result.news.map(n => ({
                title: n.title,
                sector: sector,
                source: n.source,
                timestamp: n.date,
            }));
        } catch (error) {
            console.error('RealApiService.getSectorNews error:', error);
            return [];
        }
    },

    /**
     * Run full AI analysis for a stock
     */
    runAnalysis: async (
        ticker: string,
        sector: string,
        language: string = 'German'
    ): Promise<AnalysisResult> => {
        try {
            // 1. Fetch fundamentals
            const fundamentals = await fetchJSON<{
                ticker: string;
                found: boolean;
                fundamentals?: {
                    pe_ratio: number;
                    peg_ratio: number;
                    roe: number;
                    debt_to_equity: number;
                    target_mean_price: number;
                    target_high_price: number;
                    target_low_price: number;
                    recommendation: string;
                    business_summary: string;
                    sector: string;
                };
            }>(`/api/fundamentals?ticker=${ticker}`);

            // 2. Fetch price history
            const priceHistory = await fetchJSON<{
                ticker: string;
                data: { date: string; close: number }[];
            }>(`/api/price_history?ticker=${ticker}&period=10y`);

            // 3. Request AI analysis
            const analysis = await fetchEnvelope<BackendAnalysisResponse>(
                '/api/engine/v1/analyze',
                {
                    method: 'POST',
                    body: JSON.stringify({
                        tickers: [ticker],
                        sectors: [sector],
                        language: language,
                    }),
                }
            );

            // 4. Fetch sector news
            const sectorNews = await RealApiService.getSectorNews(sector);

            // 5. Build AnalysisResult
            const fund = fundamentals.fundamentals;
            const sanitization = buildSanitizationTrace();
            const report: Report = {
                stock: ticker,
                summary: sanitizeText(analysis.summary),
                deepAnalysis: sanitizeText(analysis.essay),
                reviewData: {
                    peRatio: fund?.pe_ratio || 0,
                    pegRatio: fund?.peg_ratio || 0,
                    roe: fund?.roe || 0,
                    debtToEquity: fund?.debt_to_equity || 0,
                },
                analystRatings: {
                    mean: fund?.target_mean_price || 0,
                    high: fund?.target_high_price || 0,
                    low: fund?.target_low_price || 0,
                    recommendation: fund?.recommendation || 'N/A',
                },
                riskAssessment: {
                    level: 'Medium', // Would need AI to determine
                    description: 'Assessment based on available data.',
                },
                marketSentiment: {
                    trend: analysis.sentiment?.includes('bull') ? 'Bullish' :
                        analysis.sentiment?.includes('bear') ? 'Bearish' : 'Neutral',
                    score: 50,
                },
                businessContext: sanitizeText(fund?.business_summary || ''),
                generatedAt: analysis.generated_at,
            };

            const chartData: ChartPoint[] = priceHistory.data?.map(d => ({
                date: d.date,
                value: d.close,
            })) || [];

            return {
                report,
                stockNews: [], // Would need stock-specific news endpoint
                sectorNews,
                essay: sanitizeText(analysis.essay),
                chartData,
                dataOrigin: 'live',
                sanitization,
            };
        } catch (error) {
            console.error('RealApiService.runAnalysis error:', error);
            throw error;
        }
    },

    /**
     * Resolve language input (fuzzy matching)
     * NOTE: Kept client-side for simplicity
     */
    resolveLanguage: (input: string): string => {
        const lower = input.toLowerCase().trim();
        const map: Record<string, string> = {
            'de': 'German', 'ger': 'German', 'deutsch': 'German', 'german': 'German',
            'en': 'English', 'eng': 'English', 'englisch': 'English', 'english': 'English',
            'tr': 'Turkish', 'türkisch': 'Turkish', 'turkish': 'Turkish',
            'fr': 'French', 'französisch': 'French', 'french': 'French',
        };
        return map[lower] || input.charAt(0).toUpperCase() + input.slice(1);
    },

    /**
     * Get market sector performance
     */
    getSectorPerformance: async (period: string = '1d'): Promise<SectorPerformance[]> => {
        try {
            return await fetchEnvelope<SectorPerformance[]>(
                `/api/engine/v1/sectors/performance?period=${period}`
            );
        } catch (error) {
            console.error('RealApiService.getSectorPerformance error:', error);
            return [];
        }
    },

    /**
     * Get compact sparkline data for a ticker
     */
    getSparklineData: async (ticker: string, period: string = '1w'): Promise<SparklineResponse> => {
        try {
            return await fetchEnvelope<SparklineResponse>(
                `/api/engine/v1/stocks/${ticker}/sparkline?period=${period}`
            );
        } catch (error) {
            console.error('RealApiService.getSparklineData error:', error);
            return { ticker, period, data: [], source: 'error' };
        }
    },

    /**
     * Check backend health
     */
    checkHealth: async (): Promise<boolean> => {
        try {
            const result = await fetchJSON<{ status: string }>('/');
            return result.status === 'AI Service Online';
        } catch {
            return false;
        }
    },

    /**
     * Analyze a theme/keyword via backend
     */
    analyzeTheme: async (query: string): Promise<ThemeResult> => {
        try {
            const result = await fetchEnvelope<ThemeResult>('/v1/analyze/theme', {
                method: 'POST',
                body: JSON.stringify({ query }),
            });
            const sanitization = buildSanitizationTrace();
            return {
                ...result,
                description: sanitizeText(result.description || ''),
                essay: sanitizeText(result.essay || ''),
                dataOrigin: 'live',
                sanitization,
            };
        } catch (error) {
            console.error('RealApiService.analyzeTheme error:', error);
            throw error;
        }
    },
};

export default RealApiService;
