/**
 * Custom Hooks for Data Fetching
 * 
 * Per DESIGN.md Line 123-124:
 * - Data fetching MUST be handled via custom hooks
 * - UI components MUST NEVER perform raw fetch or business logic
 */

import { useQuery, useMutation, useQueryClient, useQueries } from '@tanstack/react-query';
import { ApiService } from '../services/ApiService';
import type { AnalysisResult, Stock, SectorPerformance, SparklineResponse } from '../types';

// ==================== Query Keys ====================
export const queryKeys = {
    analysis: (ticker: string, sector: string, language: string) =>
        ['analysis', ticker.toUpperCase(), sector.toUpperCase(), language.toUpperCase()] as const,
    stockSearch: (query: string) => ['stock', 'search', query.toLowerCase()] as const,
    stocks: () => ['stocks'] as const,
    sectors: (period: string) => ['sectors', 'performance', period.toLowerCase()] as const,
    sparkline: (ticker: string, period: string) => ['sparkline', ticker.toUpperCase(), period.toLowerCase()] as const,
};

// ==================== useAnalysis Hook ====================
interface UseAnalysisOptions {
    enabled?: boolean;
}

export function useAnalysis(
    ticker: string,
    sector: string,
    language: string,
    options: UseAnalysisOptions = {}
) {
    return useQuery({
        queryKey: queryKeys.analysis(ticker, sector, language),
        queryFn: async (): Promise<AnalysisResult> => {
            return ApiService.runAnalysis(ticker, sector, language);
        },
        enabled: options.enabled !== false && !!ticker && !!sector,
        staleTime: 5 * 60 * 1000, // 5 min - per DESIGN.md Token Usage Governance
        gcTime: 30 * 60 * 1000,   // 30 min garbage collection
        retry: 1,
    });
}

// ==================== useStockSearch Hook ====================
interface SearchResult {
    symbol: string;
    name?: string;
    sector: string;
    price?: number;
    change?: number;
    history?: number[];
    confidence?: number;
}

export function useStockSearch(query: string, options: { enabled?: boolean } = {}) {
    return useQuery({
        queryKey: queryKeys.stockSearch(query),
        queryFn: async (): Promise<SearchResult | null> => {
            if (!query || query.length < 1) return null;
            return ApiService.searchStock(query) as Promise<SearchResult | null>;
        },
        enabled: options.enabled !== false && !!query && query.length >= 1,
        staleTime: 10 * 60 * 1000, // 10 min cache for stock lookups
        gcTime: 60 * 60 * 1000,    // 1 hour
    });
}

// ==================== useStocks Hook ====================
export function useStocks() {
    return useQuery({
        queryKey: queryKeys.stocks(),
        queryFn: async (): Promise<Stock[]> => {
            // Only MockApiService has getStocks
            if ('getStocks' in ApiService) {
                return (ApiService as any).getStocks();
            }
            return [];
        },
        staleTime: Infinity, // Static data
    });
}

// ==================== useRunAnalysis Mutation ====================
export function useRunAnalysisMutation() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async ({ ticker, sector, language }: {
            ticker: string;
            sector: string;
            language: string
        }) => {
            return ApiService.runAnalysis(ticker, sector, language);
        },
        onSuccess: (data, variables) => {
            // Update cache with result
            queryClient.setQueryData(
                queryKeys.analysis(variables.ticker, variables.sector, variables.language),
                data
            );
        },
    });
}

export function useRunThemeAnalysisMutation() {
    return useMutation({
        mutationFn: async (query: string) => {
            return ApiService.analyzeTheme(query);
        },
        onSuccess: (data) => {
            // Can optionally cache or just return
            console.log("Theme Analysis Success:", data);
        }
    });
}

export function useSectorPerformance(period: string = '1d') {
    return useQuery({
        queryKey: queryKeys.sectors(period),
        queryFn: async (): Promise<SectorPerformance[]> => {
            return ApiService.getSectorPerformance(period);
        },
        staleTime: 5 * 60 * 1000, // 5 min
    });
}

export function useSparklineData(ticker: string, period: string = '1w') {
    return useQuery({
        queryKey: queryKeys.sparkline(ticker, period),
        queryFn: async (): Promise<SparklineResponse> => {
            return ApiService.getSparklineData(ticker, period);
        },
        enabled: !!ticker,
        staleTime: 5 * 60 * 1000, // 5 min
    });
}

export function useSparklineBatch(tickers: string[], period: string = '1w') {
    const queries = useQueries({
        queries: tickers.map((ticker) => ({
            queryKey: queryKeys.sparkline(ticker, period),
            queryFn: async (): Promise<SparklineResponse> => {
                return ApiService.getSparklineData(ticker, period);
            },
            enabled: !!ticker,
            staleTime: 5 * 60 * 1000,
        })),
    });

    const responses = queries.map(q => q.data).filter(Boolean) as SparklineResponse[];
    const allPoints = responses.flatMap(r => r.data || []);
    const range: [number, number] | undefined = allPoints.length
        ? [Math.min(...allPoints), Math.max(...allPoints)]
        : undefined;

    return {
        data: responses,
        range,
        isLoading: queries.some(q => q.isLoading),
    };
}

export default {
    useAnalysis,
    useStockSearch,
    useStocks,
    useSectorPerformance,
    useSparklineData,
    useSparklineBatch,
    useRunAnalysisMutation,
    useRunThemeAnalysisMutation,
};
