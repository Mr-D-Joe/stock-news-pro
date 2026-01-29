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
    themeQuery: string; // [NEW]
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
    setThemeQuery: (query: string) => void; // [NEW]

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
        themeQuery: '', // [NEW] Initial empty
    });

    // Analysis result (populated by components using TanStack Query hooks)
    const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
    const [analysisStatus, setAnalysisStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');

    // UI Setters
    // [NEW] Theme Query Setter (Mutually Exclusive with Stock)
    const setThemeQuery = (query: string) =>
        setUIState(s => ({
            ...s,
            themeQuery: query,
            selectedStock: query ? '' : s.selectedStock // Clear stock if theme set
        }));

    const setSelectedStock = (stock: string) =>
        setUIState(s => ({
            ...s,
            selectedStock: stock,
            themeQuery: stock ? '' : s.themeQuery // Clear theme if stock set
        }));

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
            setThemeQuery, // [NEW] Added to provider
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
// eslint-disable-next-line react-refresh/only-export-components
export const useAppContext = () => {
    const context = useContext(AppContext);
    if (context === undefined) {
        throw new Error('useAppContext must be used within an AppProvider');
    }
    return context;
};

// ==================== Legacy Layer Removed ====================
// All components migrated to useAppContext + TanStack Query hooks
// Per DESIGN.md L118, L123-124
