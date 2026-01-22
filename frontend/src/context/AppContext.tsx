/**
 * AppContext - UI State Management Only
 * 
 * Per DESIGN.md:
 * - Line 118: Server-state MUST be managed via TanStack Query
 * - Line 119: Local UI state MUST stay in smallest possible component scope
 * - Line 123-124: Data fetching MUST be via custom hooks
 * 
 * This context ONLY manages UI state (selected values, timeframes, etc.)
 * Data fetching is delegated to hooks in useDataFetching.ts
 */

import { createContext, useContext, useState, type ReactNode } from 'react';
import type { Timeframe, AnalysisScope, AnalysisResult } from '../types';
import { ApiService } from '../services/ApiService';

// ==================== Types ====================
interface UIState {
    selectedStock: string;
    selectedSector: string;
    selectedLanguage: string;
    selectedTimeframe: Timeframe;
    selectedScope: AnalysisScope;
}

interface AppContextType {
    // UI State
    uiState: UIState;

    // UI Setters
    setSelectedStock: (stock: string) => void;
    setSelectedSector: (sector: string) => void;
    setSelectedLanguage: (language: string) => void;
    setTimeframe: (tf: Timeframe) => void;
    setScope: (scope: AnalysisScope) => void;

    // Resolution helpers (pure functions, no fetching)
    resolveLanguage: (input: string) => string;

    // Analysis result (set by components using hooks)
    analysisResult: AnalysisResult | null;
    setAnalysisResult: (result: AnalysisResult | null) => void;
    analysisStatus: 'idle' | 'loading' | 'success' | 'error';
    setAnalysisStatus: (status: 'idle' | 'loading' | 'success' | 'error') => void;
}

// ==================== Context ====================
const AppContext = createContext<AppContextType | undefined>(undefined);

// ==================== Provider ====================
export const AppProvider = ({ children }: { children: ReactNode }) => {
    // UI State (not server data)
    const [uiState, setUIState] = useState<UIState>({
        selectedStock: 'ACME',
        selectedSector: 'Industrials',
        selectedLanguage: 'English',
        selectedTimeframe: '24H',
        selectedScope: 'Combined',
    });

    // Analysis result (populated by components using TanStack Query hooks)
    const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
    const [analysisStatus, setAnalysisStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');

    // UI Setters
    const setSelectedStock = (stock: string) =>
        setUIState(s => ({ ...s, selectedStock: stock }));

    const setSelectedSector = (sector: string) =>
        setUIState(s => ({ ...s, selectedSector: sector }));

    const setSelectedLanguage = (language: string) =>
        setUIState(s => ({ ...s, selectedLanguage: language }));

    const setTimeframe = (tf: Timeframe) =>
        setUIState(s => ({ ...s, selectedTimeframe: tf }));

    const setScope = (scope: AnalysisScope) =>
        setUIState(s => ({ ...s, selectedScope: scope }));

    // Pure resolution function (no API call - per Token Governance)
    const resolveLanguage = (input: string): string => {
        return ApiService.resolveLanguage(input);
    };

    return (
        <AppContext.Provider value={{
            uiState,
            setSelectedStock,
            setSelectedSector,
            setSelectedLanguage,
            setTimeframe,
            setScope,
            resolveLanguage,
            analysisResult,
            setAnalysisResult,
            analysisStatus,
            setAnalysisStatus,
        }}>
            {children}
        </AppContext.Provider>
    );
};

// ==================== Hook ====================
export const useAppContext = () => {
    const context = useContext(AppContext);
    if (context === undefined) {
        throw new Error('useAppContext must be used within an AppProvider');
    }
    return context;
};

// ==================== Legacy Compatibility Layer ====================
// This provides backward compatibility for existing components
// TODO: Migrate components to use new structure, then remove this
export const useLegacyAppContext = () => {
    const ctx = useAppContext();

    return {
        state: {
            selectedStock: ctx.uiState.selectedStock,
            selectedSector: ctx.uiState.selectedSector,
            selectedLanguage: ctx.uiState.selectedLanguage,
            selectedTimeframe: ctx.uiState.selectedTimeframe,
            selectedScope: ctx.uiState.selectedScope,
            analysisStatus: ctx.analysisStatus,
            analysisResult: ctx.analysisResult,
            stocks: [], // Now fetched via useStocks() hook
        },
        setStockInput: ctx.setSelectedStock,
        setSectorInput: ctx.setSelectedSector,
        setLanguageInput: ctx.setSelectedLanguage,
        setTimeframe: ctx.setTimeframe,
        setScope: ctx.setScope,
        resolveLanguageInput: async (input: string) => {
            const resolved = ctx.resolveLanguage(input);
            ctx.setSelectedLanguage(resolved);
        },
        // Real implementations for backward compatibility
        runAnalysis: async (tickerOverride?: string) => {
            const ticker = tickerOverride || ctx.uiState.selectedStock;
            const sector = ctx.uiState.selectedSector;
            const language = ctx.uiState.selectedLanguage;
            
            if (!ticker) return;
            
            ctx.setAnalysisStatus('loading');
            try {
                const result = await ApiService.runAnalysis(ticker, sector, language);
                ctx.setAnalysisResult(result);
                ctx.setAnalysisStatus('success');
            } catch (error) {
                console.error('Analysis failed:', error);
                ctx.setAnalysisStatus('error');
            }
        },
        resolveStockInput: async (input: string): Promise<string | null> => {
            if (!input) return null;
            try {
                const result = await ApiService.searchStock(input);
                if (result) {
                    const confidence = 'confidence' in result ? (result as any).confidence : 1.0;
                    if (confidence > 0.8) {
                        console.log(`[Smart Resolve] ${input} -> ${result.symbol}`);
                        ctx.setSelectedStock(result.symbol);
                        if (result.sector) {
                            ctx.setSelectedSector(result.sector);
                        }
                        return result.symbol;
                    }
                }
            } catch (e) {
                console.error('Stock resolution failed:', e);
            }
            return null;
        },
    };
};

