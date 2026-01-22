/**
 * Ticker Resolution Types
 * 
 * Per DESIGN.md:
 * - L162-166: APIs must be typed, return explicit error objects
 * - L343-346: Errors must be explicit, typed, user-visible
 * - L273: External APIs must be abstracted behind service layers
 */

// ==================== Request Types ====================

export interface TickerResolutionRequest {
    query: string;
    options?: {
        skipCache?: boolean;
        preferredProvider?: 'Yahoo' | 'FMP';
    };
}

// ==================== Result Types ====================

export interface TickerResolutionSuccess {
    type: 'success';
    symbol: string;
    name: string;
    sector: string;
    confidence: number;
    source: ProviderName;
    fromCache: boolean;
}

export interface TickerResolutionCandidates {
    type: 'candidates';
    candidates: TickerCandidate[];
    message: string;
}

export interface TickerCandidate {
    symbol: string;
    name: string;
    sector: string;
    confidence: number;
}

export type TickerResolutionResult =
    | TickerResolutionSuccess
    | TickerResolutionCandidates
    | TickerResolutionError;

// ==================== Error Types ====================

export type TickerResolutionErrorCode =
    | 'NOT_FOUND'
    | 'RATE_LIMIT'
    | 'PROVIDER_DOWN'
    | 'LOW_CONFIDENCE'
    | 'AMBIGUOUS'
    | 'INVALID_INPUT'
    | 'NETWORK_ERROR';

export interface TickerResolutionError {
    type: 'error';
    code: TickerResolutionErrorCode;
    message: string;
    suggestions?: string[];
    retryAfter?: number; // ms
}

// Helper function to create typed errors
export function createResolutionError(
    code: TickerResolutionErrorCode,
    message: string,
    options?: { suggestions?: string[]; retryAfter?: number }
): TickerResolutionError {
    return {
        type: 'error',
        code,
        message,
        ...options,
    };
}

// ==================== Provider Types ====================

export type ProviderName = 'Yahoo' | 'FMP' | 'Mock';

export interface ProviderResult {
    symbol: string;
    name: string;
    sector: string;
    confidence: number;
    raw?: unknown; // Original API response for debugging
}

export interface ProviderStatus {
    name: ProviderName;
    available: boolean;
    remainingQuota: number;
    resetAt?: string; // ISO8601
}

export interface TickerProvider {
    readonly name: ProviderName;
    search(query: string): Promise<ProviderResult | null>;
    isAvailable(): boolean;
    getRemainingQuota(): number;
    getStatus(): ProviderStatus;
}

// ==================== Cache Types ====================

export interface TickerCacheEntry {
    query_normalized: string;
    symbol: string;
    name: string;
    sector: string;
    confidence: number;
    source: ProviderName;
    timestamp: string; // ISO8601
    expiresAt: string; // ISO8601
    isNegative?: boolean; // For NOT_FOUND caching
}

export interface TickerCacheConfig {
    maxSize: number;
    ttlDays: number;
    negativeCacheTtlHours: number;
}

export const NAME_TO_SYMBOL_CACHE_CONFIG: TickerCacheConfig = {
    maxSize: 1000,
    ttlDays: 30,
    negativeCacheTtlHours: 24,
};

export const SYMBOL_TO_NAME_CACHE_CONFIG: TickerCacheConfig = {
    maxSize: 1000,
    ttlDays: 90,
    negativeCacheTtlHours: 24,
};

// ==================== Rate Limiter Types ====================

export interface RateLimiterConfig {
    maxRequestsPerSecond: number;
    maxRequestsPerDay: number;
    maxRetries: number;
    baseBackoffMs: number;
    maxBackoffMs: number;
}

export const YAHOO_RATE_CONFIG: RateLimiterConfig = {
    maxRequestsPerSecond: 5,
    maxRequestsPerDay: 500,
    maxRetries: 5,
    baseBackoffMs: 1000,
    maxBackoffMs: 60000,
};

export const FMP_RATE_CONFIG: RateLimiterConfig = {
    maxRequestsPerSecond: 2,
    maxRequestsPerDay: 250,
    maxRetries: 3,
    baseBackoffMs: 1000,
    maxBackoffMs: 30000,
};

// ==================== Utility Types ====================

export function normalizeQuery(query: string): string {
    return query.trim().toUpperCase();
}

export function isExpired(entry: TickerCacheEntry): boolean {
    return new Date(entry.expiresAt) < new Date();
}
