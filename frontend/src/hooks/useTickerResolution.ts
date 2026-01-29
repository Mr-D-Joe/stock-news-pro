/**
 * Ticker Resolution Hook
 * 
 * Per DESIGN.md:
 * - L118: Server-state MUST be managed via TanStack Query
 * - L123-124: Data fetching MUST be via custom hooks
 * - L136: Components MUST never fetch data directly
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { TickerResolutionService } from '../services/TickerResolutionService';
import type {
    TickerResolutionRequest,
    TickerResolutionResult,
    TickerResolutionErrorCode,
} from '../types/tickerResolution';

// ==================== Query Keys ====================

export const tickerResolutionKeys = {
    all: ['tickerResolution'] as const,
    resolve: (query: string) => [...tickerResolutionKeys.all, 'resolve', query.toUpperCase()] as const,
    status: () => [...tickerResolutionKeys.all, 'status'] as const,
};

// ==================== useTickerResolution Hook ====================

export interface UseTickerResolutionOptions {
    enabled?: boolean;
    skipCache?: boolean;
}

const getErrorCode = (error: unknown): TickerResolutionErrorCode | null => {
    if (!error || typeof error !== 'object' || !('code' in error)) {
        return null;
    }
    const code = (error as { code?: unknown }).code;
    return typeof code === 'string' ? (code as TickerResolutionErrorCode) : null;
};

export function useTickerResolution(
    query: string,
    options: UseTickerResolutionOptions = {}
) {
    return useQuery({
        queryKey: tickerResolutionKeys.resolve(query),
        queryFn: async (): Promise<TickerResolutionResult> => {
            return TickerResolutionService.resolve({
                query,
                options: { skipCache: options.skipCache },
            });
        },
        enabled: options.enabled !== false && !!query && query.length >= 1,
        staleTime: 5 * 60 * 1000, // 5 minutes
        gcTime: 30 * 60 * 1000,   // 30 minutes
        retry: (failureCount, error) => {
            // Don't retry on NOT_FOUND or INVALID_INPUT
            const code = getErrorCode(error);
            if (code === 'NOT_FOUND' || code === 'INVALID_INPUT') {
                return false;
            }
            return failureCount < 2;
        },
    });
}

// ==================== useTickerResolutionMutation Hook ====================

export function useTickerResolutionMutation() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (request: TickerResolutionRequest): Promise<TickerResolutionResult> => {
            return TickerResolutionService.resolve(request);
        },
        onSuccess: (data, variables) => {
            // Update cache with result
            queryClient.setQueryData(
                tickerResolutionKeys.resolve(variables.query),
                data
            );
        },
    });
}

// ==================== useTickerServiceStatus Hook ====================

export function useTickerServiceStatus() {
    return useQuery({
        queryKey: tickerResolutionKeys.status(),
        queryFn: () => TickerResolutionService.getStatus(),
        staleTime: 30 * 1000, // 30 seconds
        refetchInterval: 60 * 1000, // Refresh every minute
    });
}

// ==================== Cache Management Utilities ====================

export function useClearTickerCache() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async () => {
            TickerResolutionService.clearCache();
            return true;
        },
        onSuccess: () => {
            // Invalidate all ticker queries
            queryClient.invalidateQueries({ queryKey: tickerResolutionKeys.all });
        },
    });
}

// ==================== Helper Functions ====================

export function isResolutionSuccess(
    result: TickerResolutionResult
): result is Extract<TickerResolutionResult, { type: 'success' }> {
    return result.type === 'success';
}

export function isResolutionError(
    result: TickerResolutionResult
): result is Extract<TickerResolutionResult, { type: 'error' }> {
    return result.type === 'error';
}

export function isResolutionCandidates(
    result: TickerResolutionResult
): result is Extract<TickerResolutionResult, { type: 'candidates' }> {
    return result.type === 'candidates';
}
