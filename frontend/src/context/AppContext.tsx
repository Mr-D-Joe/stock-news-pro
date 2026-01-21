import { createContext, useContext, useState, useEffect, type ReactNode } from 'react';
import type { AppState, Timeframe, AnalysisScope } from '../types';
import { MockApiService } from '../services/MockApiService';

interface AppContextType {
    state: AppState;
    setStockInput: (input: string) => void;
    setSectorInput: (input: string) => void;
    setLanguageInput: (input: string) => void;
    setTimeframe: (tf: Timeframe) => void;
    setScope: (scope: AnalysisScope) => void;
    runAnalysis: (tickerOverride?: string) => Promise<void>;
    resolveStockInput: (input: string) => Promise<string | null>;
    resolveLanguageInput: (input: string) => Promise<void>;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export const AppProvider = ({ children }: { children: ReactNode }) => {
    const [state, setState] = useState<AppState>({
        selectedStock: "ACME",
        selectedSector: "Industrials",
        selectedLanguage: "English", // Default
        selectedTimeframe: '24H',
        selectedScope: 'Combined',
        analysisStatus: 'idle',
        analysisResult: null,
        stocks: []
    });

    // Client-Side Cache (Stores Search Hits and Analysis Results to avoid re-fetching)
    // Key format: "SEARCH:<Ticker>" or "ANALYSIS:<Ticker>:<Sector>:<Language>"
    const [cache, setCache] = useState<Map<string, any>>(new Map());

    useEffect(() => {
        MockApiService.getStocks().then(stocks => {
            setState(s => ({ ...s, stocks }));
            // Auto-Run Analysis on Mount to bind Mock Data immediately
            // runAnalysis(); // Removed auto-run as initial state has no stock
        });
    }, []);

    const setStockInput = (input: string) => setState(s => ({ ...s, selectedStock: input }));
    const setSectorInput = (input: string) => setState(s => ({ ...s, selectedSector: input }));
    const setLanguageInput = (input: string) => setState(s => ({ ...s, selectedLanguage: input }));

    // ... Timeframe/Scope Setters ...
    const setTimeframe = (tf: Timeframe) => setState(s => ({ ...s, selectedTimeframe: tf }));
    const setScope = (scope: AnalysisScope) => setState(s => ({ ...s, selectedScope: scope }));

    const runAnalysis = async (tickerOverride?: string) => {
        const targetStock = tickerOverride || state.selectedStock;
        if (!targetStock) return;

        setState(s => ({ ...s, analysisStatus: 'loading' }));
        const targetSector = state.selectedSector;
        const targetLang = state.selectedLanguage;

        // Compound Cache Key
        const cacheKey = `ANALYSIS:${targetStock.toUpperCase()}:${targetSector.toUpperCase()}:${targetLang.toUpperCase()}`;

        try {
            // 1. Check Output Cache
            if (cache.has(cacheKey)) {
                console.log(`[Cache Hit] Serving Analysis for ${cacheKey}`);
                setState(s => ({
                    ...s,
                    analysisStatus: 'success',
                    analysisResult: cache.get(cacheKey)
                }));
                return;
            }

            // 2. Resolve Alias (if not already done via smart input) - Keeping simplified here
            const resolvedSymbol = MockApiService.resolveSymbol(targetStock);

            // 3. Perform Analysis (Language Aware)
            const result = await MockApiService.runAnalysis(resolvedSymbol || targetStock, targetLang);

            // 4. Update Cache
            setCache(prev => {
                const newCache = new Map(prev);
                newCache.set(cacheKey, result);
                if (newCache.size > 50) { // Limit cache size
                    const first = newCache.keys().next().value;
                    if (first) newCache.delete(first);
                }
                return newCache;
            });

            setState(s => ({
                ...s,
                analysisStatus: 'success',
                analysisResult: result
            }));
        } catch (error) {
            console.error(error);
            setState(s => ({ ...s, analysisStatus: 'error' }));
        }
    };

    // Smart Resolution Logic for Stock
    const resolveStockInput = async (input: string): Promise<string | null> => {
        if (!input) return null;
        try {
            const result = await MockApiService.searchStock(input);
            if (result && result.confidence > 0.8) {
                console.log(`[Smart Resolve] ${input} -> ${result.symbol}`);
                const stockData = state.stocks.find(s => s.symbol === result.symbol);
                const derivedSector = stockData ? stockData.sector : (result.sector || state.selectedSector);

                setState(s => ({ ...s, selectedStock: result.symbol, selectedSector: derivedSector }));
                return result.symbol;
            }
        } catch (e) {
            console.error(e);
        }
        return null;
    };

    // Smart Resolution Logic for Language
    const resolveLanguageInput = async (input: string) => {
        if (!input) return;
        const resolved = await MockApiService.resolveLanguage(input);
        if (resolved !== state.selectedLanguage) {
            console.log(`[Lang Resolve] ${input} -> ${resolved}`);
            setState(s => ({ ...s, selectedLanguage: resolved }));
        }
    };

    return (
        <AppContext.Provider value={{
            state,
            setStockInput,
            setSectorInput,
            setLanguageInput,
            setTimeframe,
            setScope,
            runAnalysis,
            resolveStockInput,
            resolveLanguageInput
        }}>
            {children}
        </AppContext.Provider>
    );
};

export const useAppContext = () => {
    const context = useContext(AppContext);
    if (context === undefined) {
        throw new Error('useAppContext must be used within an AppProvider');
    }
    return context;
};
