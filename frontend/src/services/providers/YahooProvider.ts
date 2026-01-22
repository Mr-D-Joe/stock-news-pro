/**
 * Yahoo Finance Provider
 * 
 * Per LASTENHEFT 2.5.5:
 * - Yahoo is PRIMARY provider
 * - Rate limited: 5 req/s, 500/day
 * - Must implement TickerProvider interface
 * 
 * Per DESIGN.md:
 * - L273: External APIs must be abstracted behind service layers
 * - L271: External APIs must be rate-limited
 * - L278-280: API keys via environment variables
 */

import type {
    TickerProvider,
    ProviderResult,
    ProviderStatus,
    ProviderName
} from '../../types/tickerResolution';
import { yahooRateLimiter, RateLimitError } from '../rateLimit/RateLimiter';

// ==================== Yahoo Finance Provider ====================

class YahooFinanceProvider implements TickerProvider {
    readonly name: ProviderName = 'Yahoo';

    private lastError: Error | null = null;
    private providerDown: boolean = false;
    private downUntil: number = 0;

    // ==================== Search Implementation ====================

    async search(query: string): Promise<ProviderResult | null> {
        if (!this.isAvailable()) {
            console.warn('[Yahoo] Provider is currently unavailable');
            return null;
        }

        const normalizedQuery = query.trim().toUpperCase();

        try {
            const result = await yahooRateLimiter.execute(
                normalizedQuery,
                () => this.fetchFromYahoo(normalizedQuery)
            ) as ProviderResult | null;

            // Reset provider down status on success
            this.providerDown = false;
            this.lastError = null;

            return result;
        } catch (error) {
            if (error instanceof RateLimitError) {
                console.warn(`[Yahoo] Rate limit hit: ${error.message}`);
                throw error;
            }

            this.handleProviderError(error as Error);
            return null;
        }
    }

    // ==================== Yahoo API Call ====================

    private async fetchFromYahoo(query: string): Promise<ProviderResult | null> {
        // Yahoo Finance search API endpoint
        // Using the autoc endpoint which is publicly accessible
        const url = `https://query1.finance.yahoo.com/v1/finance/search?q=${encodeURIComponent(query)}&quotesCount=5&newsCount=0&enableFuzzyQuery=true`;

        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                },
            });

            if (!response.ok) {
                if (response.status === 429) {
                    throw new RateLimitError('Yahoo', 60); // Assume 60s retry
                }
                throw new Error(`Yahoo API error: ${response.status}`);
            }

            const data = await response.json();
            return this.parseYahooResponse(data, query);

        } catch (error) {
            if (error instanceof RateLimitError) {
                throw error;
            }
            console.error('[Yahoo] Fetch error:', error);
            throw error;
        }
    }

    // ==================== Response Parsing ====================

    private parseYahooResponse(data: YahooSearchResponse, query: string): ProviderResult | null {
        if (!data.quotes || data.quotes.length === 0) {
            return null;
        }

        // Find best match
        const quote = data.quotes[0];

        // Calculate confidence based on match quality
        const confidence = this.calculateConfidence(query, quote);

        return {
            symbol: quote.symbol,
            name: quote.shortname || quote.longname || quote.symbol,
            sector: quote.sector || quote.industry || 'Unknown',
            confidence,
            raw: quote,
        };
    }

    private calculateConfidence(query: string, quote: YahooQuote): number {
        const normalizedQuery = query.toUpperCase();
        const symbol = quote.symbol.toUpperCase();
        const name = (quote.shortname || quote.longname || '').toUpperCase();

        // Exact symbol match
        if (symbol === normalizedQuery) {
            return 1.0;
        }

        // Symbol contains query
        if (symbol.includes(normalizedQuery)) {
            return 0.95;
        }

        // Name starts with query
        if (name.startsWith(normalizedQuery)) {
            return 0.90;
        }

        // Name contains query
        if (name.includes(normalizedQuery)) {
            return 0.85;
        }

        // Fuzzy match (Yahoo found something)
        return 0.75;
    }

    // ==================== Provider Status ====================

    isAvailable(): boolean {
        if (this.providerDown && Date.now() < this.downUntil) {
            return false;
        }

        // Reset if cooldown passed
        if (this.providerDown && Date.now() >= this.downUntil) {
            this.providerDown = false;
        }

        return yahooRateLimiter.getRateLimiter().canMakeRequest();
    }

    getRemainingQuota(): number {
        return yahooRateLimiter.getRateLimiter().getRemainingQuota();
    }

    getStatus(): ProviderStatus {
        const limiterStatus = yahooRateLimiter.getStatus();
        return {
            name: this.name,
            available: this.isAvailable(),
            remainingQuota: limiterStatus.dailyRemaining,
            resetAt: limiterStatus.resetAt,
        };
    }

    // ==================== Error Handling ====================

    private handleProviderError(error: Error): void {
        this.lastError = error;
        this.providerDown = true;
        // Cooldown for 5 minutes on provider error
        this.downUntil = Date.now() + 5 * 60 * 1000;
        console.error(`[Yahoo] Provider marked as down until ${new Date(this.downUntil).toISOString()}`);
    }

    getLastError(): Error | null {
        return this.lastError;
    }
}

// ==================== Yahoo API Types ====================

interface YahooSearchResponse {
    quotes: YahooQuote[];
}

interface YahooQuote {
    symbol: string;
    shortname?: string;
    longname?: string;
    sector?: string;
    industry?: string;
    exchange?: string;
    quoteType?: string;
}

// ==================== Singleton Export ====================

export const yahooProvider = new YahooFinanceProvider();
export { YahooFinanceProvider };
