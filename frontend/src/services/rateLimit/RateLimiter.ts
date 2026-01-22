/**
 * Rate Limiter with Exponential Backoff and In-Flight De-duplication
 * 
 * Per LASTENHEFT 2.5.3:
 * - Token Bucket per provider
 * - Hard-stop at rate limit (no retry storms)
 * - Exponential backoff with jitter
 * - In-flight de-duplication
 * 
 * Per DESIGN.md:
 * - L271: External APIs must be rate-limited
 * - L234-239: Minimize calls, deduplicate identical prompts
 */

import type { RateLimiterConfig } from '../../types/tickerResolution';

// ==================== Token Bucket Rate Limiter ====================

export class TokenBucketRateLimiter {
    private tokens: number;
    private lastRefill: number;
    private dailyUsage: number;
    private dailyResetTime: number;
    private readonly config: RateLimiterConfig;
    private readonly providerName: string;

    constructor(providerName: string, config: RateLimiterConfig) {
        this.providerName = providerName;
        this.config = config;
        this.tokens = config.maxRequestsPerSecond;
        this.lastRefill = Date.now();
        this.dailyUsage = 0;
        this.dailyResetTime = this.getNextMidnight();
    }

    // ==================== Core Operations ====================

    canMakeRequest(): boolean {
        this.refillTokens();
        this.checkDailyReset();

        return this.tokens > 0 && this.dailyUsage < this.config.maxRequestsPerDay;
    }

    consumeToken(): boolean {
        if (!this.canMakeRequest()) {
            return false;
        }

        this.tokens -= 1;
        this.dailyUsage += 1;
        return true;
    }

    getRemainingQuota(): number {
        this.checkDailyReset();
        return Math.max(0, this.config.maxRequestsPerDay - this.dailyUsage);
    }

    getSecondsUntilNextToken(): number {
        if (this.tokens > 0) return 0;
        const msPerToken = 1000 / this.config.maxRequestsPerSecond;
        const elapsed = Date.now() - this.lastRefill;
        return Math.max(0, Math.ceil((msPerToken - elapsed) / 1000));
    }

    // ==================== Token Refill ====================

    private refillTokens(): void {
        const now = Date.now();
        const elapsed = now - this.lastRefill;
        const tokensToAdd = (elapsed / 1000) * this.config.maxRequestsPerSecond;

        this.tokens = Math.min(
            this.config.maxRequestsPerSecond,
            this.tokens + tokensToAdd
        );
        this.lastRefill = now;
    }

    private checkDailyReset(): void {
        if (Date.now() >= this.dailyResetTime) {
            this.dailyUsage = 0;
            this.dailyResetTime = this.getNextMidnight();
            console.log(`[RateLimiter:${this.providerName}] Daily quota reset`);
        }
    }

    private getNextMidnight(): number {
        const now = new Date();
        const midnight = new Date(now);
        midnight.setHours(24, 0, 0, 0);
        return midnight.getTime();
    }

    // ==================== Stats ====================

    getStatus(): RateLimiterStatus {
        this.refillTokens();
        this.checkDailyReset();

        return {
            provider: this.providerName,
            tokensAvailable: Math.floor(this.tokens),
            dailyRemaining: this.getRemainingQuota(),
            dailyLimit: this.config.maxRequestsPerDay,
            resetAt: new Date(this.dailyResetTime).toISOString(),
        };
    }
}

export interface RateLimiterStatus {
    provider: string;
    tokensAvailable: number;
    dailyRemaining: number;
    dailyLimit: number;
    resetAt: string;
}

// ==================== Exponential Backoff ====================

export class ExponentialBackoff {
    private retryCount: number = 0;
    private readonly config: RateLimiterConfig;

    constructor(config: RateLimiterConfig) {
        this.config = config;
    }

    reset(): void {
        this.retryCount = 0;
    }

    canRetry(): boolean {
        return this.retryCount < this.config.maxRetries;
    }

    getNextDelay(): number {
        if (!this.canRetry()) return -1;

        // Exponential backoff: baseMs * 2^retryCount + jitter
        const exponentialDelay = this.config.baseBackoffMs * Math.pow(2, this.retryCount);
        const jitter = Math.random() * 500; // 0-500ms jitter
        const delay = Math.min(exponentialDelay + jitter, this.config.maxBackoffMs);

        this.retryCount++;
        return delay;
    }

    getRetryCount(): number {
        return this.retryCount;
    }
}

// ==================== In-Flight De-duplication ====================

export class InFlightDeduplicator<T> {
    private pending: Map<string, Promise<T>> = new Map();

    /**
     * Execute a function with de-duplication.
     * If the same key is already in-flight, return the existing promise.
     */
    async dedupe(key: string, fn: () => Promise<T>): Promise<T> {
        const normalizedKey = key.trim().toUpperCase();

        // Check if request is already in-flight
        const existing = this.pending.get(normalizedKey);
        if (existing) {
            console.log(`[Dedup] Reusing in-flight request for: ${normalizedKey}`);
            return existing;
        }

        // Create new request
        const promise = fn().finally(() => {
            this.pending.delete(normalizedKey);
        });

        this.pending.set(normalizedKey, promise);
        return promise;
    }

    hasPending(key: string): boolean {
        return this.pending.has(key.trim().toUpperCase());
    }

    getPendingCount(): number {
        return this.pending.size;
    }

    clear(): void {
        this.pending.clear();
    }
}

// ==================== Combined Rate-Limited Request Handler ====================

export interface RateLimitedRequestOptions {
    skipRateLimit?: boolean;
}

export class RateLimitedRequestHandler<T> {
    private readonly rateLimiter: TokenBucketRateLimiter;
    private readonly deduplicator: InFlightDeduplicator<T>;
    private readonly providerName: string;

    constructor(providerName: string, config: RateLimiterConfig) {
        this.providerName = providerName;
        this.rateLimiter = new TokenBucketRateLimiter(providerName, config);
        this.deduplicator = new InFlightDeduplicator<T>();
    }

    async execute(
        key: string,
        fn: () => Promise<T>,
        options: RateLimitedRequestOptions = {}
    ): Promise<T> {
        return this.deduplicator.dedupe(key, async () => {
            // Check rate limit
            if (!options.skipRateLimit && !this.rateLimiter.consumeToken()) {
                throw new RateLimitError(
                    this.providerName,
                    this.rateLimiter.getSecondsUntilNextToken()
                );
            }

            return fn();
        });
    }

    getRateLimiter(): TokenBucketRateLimiter {
        return this.rateLimiter;
    }

    getStatus(): RateLimiterStatus {
        return this.rateLimiter.getStatus();
    }
}

// ==================== Error Types ====================

export class RateLimitError extends Error {
    readonly provider: string;
    readonly retryAfterSeconds: number;

    constructor(provider: string, retryAfterSeconds: number) {
        super(`Rate limit exceeded for ${provider}. Retry after ${retryAfterSeconds}s`);
        this.name = 'RateLimitError';
        this.provider = provider;
        this.retryAfterSeconds = retryAfterSeconds;
    }
}

// ==================== Singleton Instances ====================

import { YAHOO_RATE_CONFIG, FMP_RATE_CONFIG } from '../../types/tickerResolution';

export const yahooRateLimiter = new RateLimitedRequestHandler<unknown>(
    'Yahoo',
    YAHOO_RATE_CONFIG
);

export const fmpRateLimiter = new RateLimitedRequestHandler<unknown>(
    'FMP',
    FMP_RATE_CONFIG
);
