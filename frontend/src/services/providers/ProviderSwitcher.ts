/**
 * Provider Switcher
 * 
 * Per LASTENHEFT 2.5.5:
 * - Yahoo is PRIMARY provider
 * - FMP is Optional Premium (later)
 * - Switching logic: Yahoo → Cache → FMP → Error
 * 
 * Per DESIGN.md:
 * - L273: External APIs must be abstracted
 * - L152: Never return silent fallback data
 */

import type {
    TickerProvider,
    ProviderResult,
    ProviderStatus,
    ProviderName,
    TickerResolutionError,
} from '../../types/tickerResolution';
import { createResolutionError } from '../../types/tickerResolution';
import { yahooProvider } from './YahooProvider';
import { RateLimitError } from '../rateLimit/RateLimiter';

// ==================== Provider Switcher ====================

class ProviderSwitcher {
    private providers: Map<ProviderName, TickerProvider> = new Map();
    private providerOrder: ProviderName[] = ['Yahoo']; // FMP added when available

    constructor() {
        this.providers.set('Yahoo', yahooProvider);
        // FMP provider will be added later when free tier is confirmed
    }

    // ==================== Main Search ====================

    async search(query: string): Promise<ProviderSearchResult> {
        const normalizedQuery = query.trim().toUpperCase();

        if (!normalizedQuery || normalizedQuery.length < 1) {
            return {
                success: false,
                error: createResolutionError('INVALID_INPUT', 'Query too short'),
            };
        }

        // Try providers in order
        for (const providerName of this.providerOrder) {
            const provider = this.providers.get(providerName);
            if (!provider) continue;

            if (!provider.isAvailable()) {
                console.log(`[ProviderSwitcher] ${providerName} not available, trying next...`);
                continue;
            }

            try {
                const result = await provider.search(normalizedQuery);

                if (result) {
                    return {
                        success: true,
                        result,
                        provider: providerName,
                    };
                } else {
                    // Provider returned null = not found
                    return {
                        success: false,
                        error: createResolutionError(
                            'NOT_FOUND',
                            `No results found for "${query}"`,
                            { suggestions: this.getSuggestions(query) }
                        ),
                        provider: providerName,
                    };
                }
            } catch (error) {
                if (error instanceof RateLimitError) {
                    return {
                        success: false,
                        error: createResolutionError(
                            'RATE_LIMIT',
                            error.message,
                            { retryAfter: error.retryAfterSeconds * 1000 }
                        ),
                        provider: providerName,
                    };
                }

                console.error(`[ProviderSwitcher] ${providerName} failed:`, error);
                // Try next provider
                continue;
            }
        }

        // All providers failed
        return {
            success: false,
            error: createResolutionError(
                'PROVIDER_DOWN',
                'All ticker resolution providers are currently unavailable'
            ),
        };
    }

    // ==================== Provider Management ====================

    getAvailableProviders(): ProviderName[] {
        return this.providerOrder.filter(name => {
            const provider = this.providers.get(name);
            return provider?.isAvailable() ?? false;
        });
    }

    getAllProviderStatus(): ProviderStatus[] {
        return Array.from(this.providers.values()).map(p => p.getStatus());
    }

    isAnyProviderAvailable(): boolean {
        return this.getAvailableProviders().length > 0;
    }

    // ==================== Suggestions ====================

    private getSuggestions(query: string): string[] {
        // Common typo corrections
        const suggestions: string[] = [];
        const q = query.toUpperCase();

        // Known company aliases
        const knownMappings: Record<string, string[]> = {
            'GOOGLE': ['GOOGL', 'GOOG', 'Alphabet Inc.'],
            'ALPHABET': ['GOOGL', 'GOOG'],
            'APPLE': ['AAPL'],
            'MICROSOFT': ['MSFT'],
            'AMAZON': ['AMZN'],
            'FACEBOOK': ['META'],
            'TESLA': ['TSLA'],
            'NVIDIA': ['NVDA'],
        };

        for (const [name, symbols] of Object.entries(knownMappings)) {
            if (q.includes(name) || name.includes(q)) {
                suggestions.push(...symbols);
            }
        }

        return suggestions.slice(0, 3);
    }

    // ==================== FMP Registration (Future) ====================

    registerFMPProvider(provider: TickerProvider): void {
        this.providers.set('FMP', provider);
        this.providerOrder = ['Yahoo', 'FMP']; // Yahoo still primary
        console.log('[ProviderSwitcher] FMP provider registered');
    }
}

// ==================== Types ====================

export interface ProviderSearchResult {
    success: boolean;
    result?: ProviderResult;
    error?: TickerResolutionError;
    provider?: ProviderName;
}

// ==================== Singleton Export ====================

export const providerSwitcher = new ProviderSwitcher();
export { ProviderSwitcher };
