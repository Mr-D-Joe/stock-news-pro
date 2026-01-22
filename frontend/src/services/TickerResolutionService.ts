/**
 * Ticker Resolution Service
 * 
 * Per DESIGN.md:
 * - L205-206: All external calls must be wrapped in typed service layer
 * - L274: Never call external APIs from UI components
 * - L118: Server-state via TanStack Query (hook will use this service)
 * 
 * Per LASTENHEFT 2.5:
 * - Cache-first strategy
 * - Provider fallback
 * - Explicit error handling
 */

import type {
    TickerResolutionRequest,
    TickerResolutionResult,
    ProviderName,
} from '../types/tickerResolution';
import {
    createResolutionError,
    normalizeQuery,
} from '../types/tickerResolution';
import { nameToSymbolCache, symbolToNameCache } from './cache/TickerCache';
import { providerSwitcher } from './providers/ProviderSwitcher';
import { isUsingRealApi } from './ApiService';

// ==================== Main Service ====================

class TickerResolutionServiceImpl {

    // ==================== Main Resolution Method ====================

    async resolve(request: TickerResolutionRequest): Promise<TickerResolutionResult> {
        const { query, options = {} } = request;
        const normalizedQuery = normalizeQuery(query);

        if (!normalizedQuery || normalizedQuery.length < 1) {
            return createResolutionError('INVALID_INPUT', 'Please enter a stock symbol or company name');
        }

        // DEV MODE: Use mock resolution
        if (!isUsingRealApi()) {
            return this.resolveMock(normalizedQuery);
        }

        // REAL MODE: Cache → Provider → Cache Write
        return this.resolveReal(normalizedQuery, options.skipCache ?? false);
    }

    // ==================== Real Mode Resolution ====================

    private async resolveReal(
        normalizedQuery: string,
        skipCache: boolean
    ): Promise<TickerResolutionResult> {

        // Step 1: Check cache (unless skip requested)
        if (!skipCache) {
            const cached = nameToSymbolCache.get(normalizedQuery);
            if (cached) {
                if (cached.isNegative) {
                    return createResolutionError(
                        'NOT_FOUND',
                        `No results found for "${normalizedQuery}" (cached)`
                    );
                }

                console.log(`[TickerService] Cache hit for: ${normalizedQuery}`);
                return {
                    type: 'success',
                    symbol: cached.symbol,
                    name: cached.name,
                    sector: cached.sector,
                    confidence: cached.confidence,
                    source: cached.source,
                    fromCache: true,
                };
            }
        }

        // Step 2: Query providers
        const searchResult = await providerSwitcher.search(normalizedQuery);

        if (!searchResult.success || !searchResult.result) {
            // Cache negative result if NOT_FOUND
            if (searchResult.error?.code === 'NOT_FOUND') {
                this.cacheNegativeResult(normalizedQuery, searchResult.provider || 'Yahoo');
            }

            return searchResult.error || createResolutionError(
                'PROVIDER_DOWN',
                'Unable to resolve ticker'
            );
        }

        const { result, provider } = searchResult;

        // Step 3: Check confidence threshold
        if (result.confidence < 0.85) {
            return {
                type: 'candidates',
                candidates: [{
                    symbol: result.symbol,
                    name: result.name,
                    sector: result.sector,
                    confidence: result.confidence,
                }],
                message: `Low confidence match. Did you mean ${result.symbol} (${result.name})?`,
            };
        }

        // Step 4: Cache successful result
        this.cacheResult(normalizedQuery, result, provider!);

        // Step 5: Return success
        return {
            type: 'success',
            symbol: result.symbol,
            name: result.name,
            sector: result.sector,
            confidence: result.confidence,
            source: provider!,
            fromCache: false,
        };
    }

    // ==================== Mock Mode Resolution ====================

    private resolveMock(normalizedQuery: string): TickerResolutionResult {
        // Use existing MockApiService logic
        // This is a simplified version for DEV_MODE
        const mockMappings: Record<string, { symbol: string; name: string; sector: string }> = {
            // Technology (US)
            'AAPL': { symbol: 'AAPL', name: 'Apple Inc.', sector: 'Technology' },
            'APPLE': { symbol: 'AAPL', name: 'Apple Inc.', sector: 'Technology' },
            'MSFT': { symbol: 'MSFT', name: 'Microsoft Corporation', sector: 'Technology' },
            'MICROSOFT': { symbol: 'MSFT', name: 'Microsoft Corporation', sector: 'Technology' },
            'GOOGL': { symbol: 'GOOGL', name: 'Alphabet Inc.', sector: 'Technology' },
            'GOOG': { symbol: 'GOOG', name: 'Alphabet Inc.', sector: 'Technology' },
            'GOOGLE': { symbol: 'GOOG', name: 'Alphabet Inc.', sector: 'Technology' },
            'ALPHABET': { symbol: 'GOOG', name: 'Alphabet Inc.', sector: 'Technology' },
            'AMZN': { symbol: 'AMZN', name: 'Amazon.com Inc.', sector: 'Consumer Cyclical' },
            'AMAZON': { symbol: 'AMZN', name: 'Amazon.com Inc.', sector: 'Consumer Cyclical' },
            'NVDA': { symbol: 'NVDA', name: 'NVIDIA Corporation', sector: 'Technology' },
            'NVIDIA': { symbol: 'NVDA', name: 'NVIDIA Corporation', sector: 'Technology' },
            'META': { symbol: 'META', name: 'Meta Platforms Inc.', sector: 'Technology' },
            'FACEBOOK': { symbol: 'META', name: 'Meta Platforms Inc.', sector: 'Technology' },
            'TSLA': { symbol: 'TSLA', name: 'Tesla Inc.', sector: 'Consumer Cyclical' },
            'TESLA': { symbol: 'TSLA', name: 'Tesla Inc.', sector: 'Consumer Cyclical' },
            'NFLX': { symbol: 'NFLX', name: 'Netflix Inc.', sector: 'Communication Services' },

            // Pharma / Healthcare (Global)
            'LLY': { symbol: 'LLY', name: 'Eli Lilly and Company', sector: 'Healthcare' },
            'ELI': { symbol: 'LLY', name: 'Eli Lilly and Company', sector: 'Healthcare' },
            'LILLY': { symbol: 'LLY', name: 'Eli Lilly and Company', sector: 'Healthcare' },
            'NVO': { symbol: 'NVO', name: 'Novo Nordisk A/S', sector: 'Healthcare' },
            'NOVO': { symbol: 'NVO', name: 'Novo Nordisk A/S', sector: 'Healthcare' },
            'AZN': { symbol: 'AZN', name: 'AstraZeneca PLC', sector: 'Healthcare' },
            'ASTRA': { symbol: 'AZN', name: 'AstraZeneca PLC', sector: 'Healthcare' },
            'PFE': { symbol: 'PFE', name: 'Pfizer Inc.', sector: 'Healthcare' },
            'PFIZER': { symbol: 'PFE', name: 'Pfizer Inc.', sector: 'Healthcare' },
            'MRK': { symbol: 'MRK', name: 'Merck & Co. Inc.', sector: 'Healthcare' },
            'MERCK': { symbol: 'MRK', name: 'Merck & Co. Inc.', sector: 'Healthcare' },
            'JNJ': { symbol: 'JNJ', name: 'Johnson & Johnson', sector: 'Healthcare' },
            'ROG': { symbol: 'ROG', name: 'Roche Holding AG', sector: 'Healthcare' },
            'ROCHE': { symbol: 'ROG', name: 'Roche Holding AG', sector: 'Healthcare' },
            'ABSI': { symbol: 'ABSI', name: 'Absci Corp', sector: 'Healthcare' },

            // Finance
            'JPM': { symbol: 'JPM', name: 'JPMorgan Chase & Co.', sector: 'Financial Services' },
            'BAC': { symbol: 'BAC', name: 'Bank of America Corp', sector: 'Financial Services' },
            'V': { symbol: 'V', name: 'Visa Inc.', sector: 'Financial Services' },
            'MA': { symbol: 'MA', name: 'Mastercard Inc.', sector: 'Financial Services' },

            // Industrial / Other
            'BA': { symbol: 'BA', name: 'Boeing Company', sector: 'Industrials' },
            'CAT': { symbol: 'CAT', name: 'Caterpillar Inc.', sector: 'Industrials' },
            'DIS': { symbol: 'DIS', name: 'Walt Disney Company', sector: 'Communication Services' },
            'KO': { symbol: 'KO', name: 'Coca-Cola Company', sector: 'Consumer Defensive' },
            'ACME': { symbol: 'ACME', name: 'ACME Corp', sector: 'Industrials' },
        };

        const match = mockMappings[normalizedQuery];
        if (match) {
            return {
                type: 'success',
                symbol: match.symbol,
                name: match.name,
                sector: match.sector,
                confidence: 1.0,
                source: 'Mock',
                fromCache: false,
            };
        }

        // Fuzzy match for typos
        for (const [key, value] of Object.entries(mockMappings)) {
            if (this.levenshteinDistance(normalizedQuery, key) <= 2) {
                return {
                    type: 'success',
                    symbol: value.symbol,
                    name: value.name,
                    sector: value.sector,
                    confidence: 0.8,
                    source: 'Mock',
                    fromCache: false,
                };
            }
        }

        return createResolutionError(
            'NOT_FOUND',
            `Symbol "${normalizedQuery}" not found in DEV_MODE mocks. Try: AAPL, MSFT, LLY, NVO...`,
            { suggestions: Object.keys(mockMappings).slice(0, 5) }
        );
    }

    // ==================== Cache Helpers ====================

    private cacheResult(
        query: string,
        result: { symbol: string; name: string; sector: string; confidence: number },
        source: ProviderName
    ): void {
        // Cache name → symbol
        nameToSymbolCache.set(query, {
            symbol: result.symbol,
            name: result.name,
            sector: result.sector,
            confidence: result.confidence,
            source,
        });

        // Cache symbol → name
        symbolToNameCache.set(result.symbol, {
            symbol: result.symbol,
            name: result.name,
            sector: result.sector,
            confidence: 1.0,
            source,
        });

        // Persist to localStorage
        nameToSymbolCache.saveToLocalStorage();
        symbolToNameCache.saveToLocalStorage();
    }

    private cacheNegativeResult(query: string, source: ProviderName): void {
        nameToSymbolCache.set(
            query,
            { symbol: '', name: '', sector: '', confidence: 0, source },
            true // isNegative
        );
        nameToSymbolCache.saveToLocalStorage();
    }

    // ==================== Utility ====================

    private levenshteinDistance(a: string, b: string): number {
        const matrix: number[][] = [];
        for (let i = 0; i <= b.length; i++) matrix[i] = [i];
        for (let j = 0; j <= a.length; j++) matrix[0][j] = j;

        for (let i = 1; i <= b.length; i++) {
            for (let j = 1; j <= a.length; j++) {
                if (b.charAt(i - 1) === a.charAt(j - 1)) {
                    matrix[i][j] = matrix[i - 1][j - 1];
                } else {
                    matrix[i][j] = Math.min(
                        matrix[i - 1][j - 1] + 1,
                        matrix[i][j - 1] + 1,
                        matrix[i - 1][j] + 1
                    );
                }
            }
        }
        return matrix[b.length][a.length];
    }

    // ==================== Status ====================

    getStatus() {
        return {
            mode: isUsingRealApi() ? 'REAL' : 'DEV',
            providers: providerSwitcher.getAllProviderStatus(),
            cache: {
                nameToSymbol: nameToSymbolCache.getStats(),
                symbolToName: symbolToNameCache.getStats(),
            },
        };
    }

    clearCache(): void {
        nameToSymbolCache.clear();
        symbolToNameCache.clear();
        nameToSymbolCache.saveToLocalStorage();
        symbolToNameCache.saveToLocalStorage();
        console.log('[TickerService] Cache cleared');
    }
}

// ==================== Singleton Export ====================

export const TickerResolutionService = new TickerResolutionServiceImpl();
