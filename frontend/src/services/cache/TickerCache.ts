/**
 * Ticker Resolution Cache
 * 
 * Per LASTENHEFT 2.5.2:
 * - FIFO eviction (1000 entries max)
 * - TTL: name_to_symbol 30 days, symbol_to_name 90 days
 * - Negative caching for NOT_FOUND (24h)
 * - Persistence: Tauri FS (primary), localStorage (warm-start)
 * 
 * Per DESIGN.md:
 * - L187-191: Tauri backend is Single Source of Truth for persistence
 * - L272: External APIs must be cached
 */

import type {
    TickerCacheEntry,
    TickerCacheConfig,
    ProviderName
} from '../../types/tickerResolution';
import { isExpired, normalizeQuery } from '../../types/tickerResolution';

// ==================== Cache Implementation ====================

export class TickerCache {
    private entries: Map<string, TickerCacheEntry> = new Map();
    private insertionOrder: string[] = []; // For FIFO eviction
    private readonly config: TickerCacheConfig;
    private readonly cacheKey: string;

    constructor(cacheKey: string, config: TickerCacheConfig) {
        this.cacheKey = cacheKey;
        this.config = config;
    }

    // ==================== Core Operations ====================

    get(query: string): TickerCacheEntry | null {
        const key = normalizeQuery(query);
        const entry = this.entries.get(key);

        if (!entry) {
            return null;
        }

        if (isExpired(entry)) {
            this.delete(key);
            return null;
        }

        return entry;
    }

    set(
        query: string,
        data: {
            symbol: string;
            name: string;
            sector: string;
            confidence: number;
            source: ProviderName;
        },
        isNegative: boolean = false
    ): void {
        const key = normalizeQuery(query);
        const now = new Date();

        // Calculate TTL
        const ttlMs = isNegative
            ? this.config.negativeCacheTtlHours * 60 * 60 * 1000
            : this.config.ttlDays * 24 * 60 * 60 * 1000;

        const expiresAt = new Date(now.getTime() + ttlMs);

        const entry: TickerCacheEntry = {
            query_normalized: key,
            symbol: data.symbol,
            name: data.name,
            sector: data.sector,
            confidence: data.confidence,
            source: data.source,
            timestamp: now.toISOString(),
            expiresAt: expiresAt.toISOString(),
            isNegative,
        };

        // Check if key already exists
        if (this.entries.has(key)) {
            // Update existing entry (don't change order)
            this.entries.set(key, entry);
        } else {
            // New entry - check capacity and evict if needed
            if (this.entries.size >= this.config.maxSize) {
                this.evictOldest();
            }
            this.entries.set(key, entry);
            this.insertionOrder.push(key);
        }
    }

    delete(key: string): boolean {
        const normalizedKey = normalizeQuery(key);
        const deleted = this.entries.delete(normalizedKey);
        if (deleted) {
            const index = this.insertionOrder.indexOf(normalizedKey);
            if (index > -1) {
                this.insertionOrder.splice(index, 1);
            }
        }
        return deleted;
    }

    clear(): void {
        this.entries.clear();
        this.insertionOrder = [];
    }

    // ==================== FIFO Eviction ====================

    private evictOldest(): void {
        if (this.insertionOrder.length === 0) return;

        const oldestKey = this.insertionOrder.shift();
        if (oldestKey) {
            this.entries.delete(oldestKey);
        }
    }

    // ==================== Stats & Inspection ====================

    get size(): number {
        return this.entries.size;
    }

    get maxSize(): number {
        return this.config.maxSize;
    }

    getStats(): CacheStats {
        let expiredCount = 0;
        let negativeCount = 0;

        for (const entry of this.entries.values()) {
            if (isExpired(entry)) expiredCount++;
            if (entry.isNegative) negativeCount++;
        }

        return {
            totalEntries: this.entries.size,
            maxEntries: this.config.maxSize,
            expiredEntries: expiredCount,
            negativeEntries: negativeCount,
        };
    }

    getEntries(): Array<[string, TickerCacheEntry]> {
        return Array.from(this.entries.entries());
    }

    // ==================== Persistence ====================

    toJSON(): string {
        return JSON.stringify({
            entries: Array.from(this.entries.entries()),
            insertionOrder: this.insertionOrder,
        });
    }

    static fromJSON(
        json: string,
        cacheKey: string,
        config: TickerCacheConfig
    ): TickerCache {
        const cache = new TickerCache(cacheKey, config);

        try {
            const data = JSON.parse(json);
            if (data.entries && Array.isArray(data.entries)) {
                for (const [key, entry] of data.entries) {
                    cache.entries.set(key, entry);
                }
            }
            if (data.insertionOrder && Array.isArray(data.insertionOrder)) {
                cache.insertionOrder = data.insertionOrder;
            }

            // Clean expired entries on load
            cache.cleanExpired();
        } catch (e) {
            console.warn(`[TickerCache] Failed to parse cache JSON for ${cacheKey}:`, e);
        }

        return cache;
    }

    private cleanExpired(): void {
        const keysToDelete: string[] = [];

        for (const [key, entry] of this.entries.entries()) {
            if (isExpired(entry)) {
                keysToDelete.push(key);
            }
        }

        for (const key of keysToDelete) {
            this.delete(key);
        }
    }

    // ==================== localStorage Warm-Start ====================

    saveToLocalStorage(): void {
        try {
            localStorage.setItem(this.cacheKey, this.toJSON());
        } catch (e) {
            console.warn(`[TickerCache] Failed to save to localStorage:`, e);
        }
    }

    static loadFromLocalStorage(
        cacheKey: string,
        config: TickerCacheConfig
    ): TickerCache {
        try {
            const json = localStorage.getItem(cacheKey);
            if (json) {
                return TickerCache.fromJSON(json, cacheKey, config);
            }
        } catch (e) {
            console.warn(`[TickerCache] Failed to load from localStorage:`, e);
        }
        return new TickerCache(cacheKey, config);
    }
}

// ==================== Types ====================

export interface CacheStats {
    totalEntries: number;
    maxEntries: number;
    expiredEntries: number;
    negativeEntries: number;
}

// ==================== Singleton Instances ====================

import {
    NAME_TO_SYMBOL_CACHE_CONFIG,
    SYMBOL_TO_NAME_CACHE_CONFIG
} from '../../types/tickerResolution';

export const nameToSymbolCache = new TickerCache(
    'ticker_name_to_symbol',
    NAME_TO_SYMBOL_CACHE_CONFIG
);

export const symbolToNameCache = new TickerCache(
    'ticker_symbol_to_name',
    SYMBOL_TO_NAME_CACHE_CONFIG
);

// Initialize from localStorage on module load (warm-start)
if (typeof window !== 'undefined' && window.localStorage) {
    const savedN2S = localStorage.getItem('ticker_name_to_symbol');
    if (savedN2S) {
        const loaded = TickerCache.fromJSON(savedN2S, 'ticker_name_to_symbol', NAME_TO_SYMBOL_CACHE_CONFIG);
        // Transfer entries
        for (const [key, entry] of loaded.getEntries()) {
            nameToSymbolCache.set(key, entry, entry.isNegative);
        }
    }

    const savedS2N = localStorage.getItem('ticker_symbol_to_name');
    if (savedS2N) {
        const loaded = TickerCache.fromJSON(savedS2N, 'ticker_symbol_to_name', SYMBOL_TO_NAME_CACHE_CONFIG);
        for (const [key, entry] of loaded.getEntries()) {
            symbolToNameCache.set(key, entry, entry.isNegative);
        }
    }
}
