/**
 * TopBar Component - DESIGN.md Compliant
 * 
 * Per DESIGN.md:
 * - L118: Server-state via TanStack Query
 * - L123: Data fetching via custom hooks
 * - L136: Components never fetch data directly
 */

import React, { useState } from 'react';
import { Globe, Play, Loader2, Search, PieChart, FlaskConical, Radio } from 'lucide-react';
import { useAppContext } from '../context/AppContext';
import { useRunAnalysisMutation, useRunThemeAnalysisMutation } from '../hooks/useDataFetching';
import { Lightbulb } from 'lucide-react';

import { useTickerResolutionMutation, isResolutionSuccess } from '../hooks/useTickerResolution';
import { isUsingRealApi } from '../services/ApiService';
import { cn } from '@/lib/utils';

export const TopBar: React.FC = () => {
    // UI State from Context (per DESIGN.md L119)
    const {
        uiState,
        setSelectedStock,
        setSelectedSector,
        setSelectedLanguage,
        resolveLanguage,
        setAnalysisResult,
        setAnalysisStatus,
        analysisStatus,
        setThemeQuery, // [NEW]
    } = useAppContext();

    const { selectedStock, selectedSector, selectedLanguage } = uiState;

    // Local state for input (before resolution)
    const [stockInput, setStockInput] = useState(selectedStock);

    // TanStack Query Mutation for Analysis (per DESIGN.md L118)
    const analysisMutation = useRunAnalysisMutation();
    const themeAnalysisMutation = useRunThemeAnalysisMutation(); // [NEW]
    const resolutionMutation = useTickerResolutionMutation();

    // Handle stock resolution and analysis
    const handleResolveAndAnalyze = async () => {
        // [NEW] Check for Theme Query first
        if (uiState.themeQuery) {
            themeAnalysisMutation.mutate(uiState.themeQuery, {
                onSuccess: (result) => {
                    // Adapt ThemeResult to AnalysisResult structure if needed, or store it
                    // For now, let's assume result IS AnalysisResult compatible or we store explicitly
                    setAnalysisResult({
                        report: {
                            stock: uiState.themeQuery,
                            summary: result.description,
                            deepAnalysis: result.essay,
                            reviewData: {} as any,
                            analystRatings: {} as any,
                            riskAssessment: {} as any,
                            marketSentiment: {} as any,
                            businessContext: "",
                            generatedAt: result.generated_at
                        },
                        stockNews: [],
                        sectorNews: [],
                        essay: result.essay,
                        chartData: [],
                        themeResult: result // Store the specific theme data
                    });
                    setAnalysisStatus('success');
                }
            });
            setAnalysisStatus('loading');
            return;
        }

        // Existing Stock Logic
        analysisMutation.mutate(
            { ticker: stockInput || selectedStock, sector: selectedSector, language: selectedLanguage },
            {
                onSuccess: (result) => {
                    setAnalysisResult(result);
                    setAnalysisStatus('success');
                },
                onError: () => {
                    setAnalysisStatus('error');
                },
            }
        );
        setAnalysisStatus('loading');
    };

    // Handle stock input blur - resolve the symbol
    const handleStockBlur = () => {
        const normalized = stockInput.toUpperCase().trim();

        // Only resolve if meaningful change
        if (normalized && normalized.length > 1) {
            resolutionMutation.mutate(
                { query: normalized },
                {
                    onSuccess: (result) => {
                        if (isResolutionSuccess(result)) {
                            // Update UI with resolved data
                            setStockInput(result.symbol); // Canonical symbol
                            setSelectedStock(result.symbol);

                            // Auto-fill sector if available
                            if (result.sector && result.sector !== 'Unknown') {
                                setSelectedSector(result.sector);
                            }
                            console.log(`[TopBar] Resolved ${normalized} -> ${result.symbol} (${result.name})`);
                        }
                    },
                    onError: (err) => {
                        console.warn('[TopBar] Resolution failed:', err);
                    }
                }
            );
        }

        if (normalized && normalized !== selectedStock) {
            setSelectedStock(normalized);
        }
    };

    // Handle language blur
    const handleLanguageBlur = () => {
        const resolved = resolveLanguage(selectedLanguage);
        if (resolved !== selectedLanguage) {
            setSelectedLanguage(resolved);
        }
    };

    return (
        <div className="w-full bg-white border-b border-gray-200 p-4 shadow-sm flex items-center justify-between gap-4 sticky top-0 z-50">

            {/* Left: Inputs */}
            <div className="flex items-center gap-4 flex-1">

                {/* Stock Input */}
                <div className="relative w-48">
                    <div className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
                        <Search className="h-4 w-4" />
                    </div>
                    <input
                        type="text"
                        className="w-full pl-9 pr-2 py-2 rounded-lg bg-slate-50 border border-gray-200 text-sm font-bold text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500 placeholder:text-gray-400 uppercase"
                        placeholder="SYMBOL / ALIAS"
                        value={stockInput}
                        onChange={(e) => {
                            const newValue = e.target.value;
                            setStockInput(newValue);
                            setSelectedStock(newValue);
                            // Clear old result when ticker changes
                            if (newValue.toUpperCase() !== selectedStock.toUpperCase()) {
                                setAnalysisResult(null);
                                setAnalysisStatus('idle');
                            }
                        }}
                        onFocus={(e) => e.target.select()}
                        onClick={(e) => e.currentTarget.select()}
                        onMouseUp={(e) => e.preventDefault()}
                        onBlur={handleStockBlur}
                        onKeyDown={(e) => {
                            if (e.key === 'Enter') {
                                e.currentTarget.blur();
                                handleResolveAndAnalyze();
                            }
                        }}
                    />
                </div>

                {/* [NEW] Theme Input (Mutually Exclusive) */}
                <div className="relative w-48" title="Themen-Suche (z.B. 'AI', 'War'). Löscht Aktien-Eingabe.">
                    <div className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
                        <Lightbulb className="h-4 w-4" />
                    </div>
                    <input
                        type="text"
                        className="w-full pl-9 pr-2 py-2 rounded-lg bg-slate-50 border border-gray-200 text-sm font-bold text-slate-900 focus:outline-none focus:ring-2 focus:ring-purple-500 placeholder:text-gray-400"
                        placeholder="THEME / TREND"
                        value={uiState.themeQuery}
                        onChange={(e) => {
                            // Context setter handles mutual exclusion (clears Stock)
                            setThemeQuery(e.target.value);
                            setStockInput(''); // Clear local stock input too
                        }}
                        onKeyDown={(e) => {
                            if (e.key === 'Enter') {
                                e.currentTarget.blur();
                                handleResolveAndAnalyze();
                            }
                        }}
                    />
                </div>

                {/* Sector Input */}
                <div className="relative w-48">
                    <div className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
                        <PieChart className="h-4 w-4" />
                    </div>
                    <input
                        type="text"
                        className="w-full pl-9 pr-2 py-2 rounded-lg bg-slate-50 border border-gray-200 text-sm font-medium text-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500 placeholder:text-gray-400 uppercase"
                        placeholder="SECTOR"
                        value={selectedSector}
                        onChange={(e) => setSelectedSector(e.target.value)}
                        onFocus={(e) => e.target.select()}
                        onClick={(e) => e.currentTarget.select()}
                        onMouseUp={(e) => e.preventDefault()}
                    />
                </div>

                {/* Language Input */}
                <div className="relative w-32">
                    <div className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
                        <Globe className="h-4 w-4" />
                    </div>
                    <input
                        type="text"
                        className="w-full pl-9 pr-2 py-2 rounded-lg bg-slate-50 border border-gray-200 text-sm font-medium text-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500 placeholder:text-gray-400"
                        placeholder="LANG"
                        value={selectedLanguage}
                        onChange={(e) => setSelectedLanguage(e.target.value)}
                        onFocus={(e) => e.target.select()}
                        onClick={(e) => e.currentTarget.select()}
                        onMouseUp={(e) => e.preventDefault()}
                        onBlur={handleLanguageBlur}
                        onKeyDown={(e) => {
                            if (e.key === 'Enter') {
                                e.currentTarget.blur();
                                handleLanguageBlur();
                            }
                        }}
                    />
                </div>

            </div>

            {/* ACTION AREA */}
            <div className="flex items-center gap-4">
                <button
                    disabled={(!selectedStock && !uiState.themeQuery) || analysisStatus === 'loading' || analysisMutation.isPending || themeAnalysisMutation.isPending}
                    onClick={handleResolveAndAnalyze}
                    className={cn(
                        "flex items-center gap-2 px-6 py-2 rounded-lg text-sm font-bold shadow-sm transition-all min-w-[150px] justify-center",
                        (!selectedStock && !uiState.themeQuery)
                            ? "bg-gray-100 text-gray-400 cursor-not-allowed"
                            : "bg-blue-600 text-white hover:bg-blue-700 shadow-blue-200 hover:shadow-md active:translate-y-0.5"
                    )}
                >
                    {(analysisStatus === 'loading' || analysisMutation.isPending || themeAnalysisMutation.isPending) ? (
                        <>
                            <Loader2 className="h-4 w-4 animate-spin" />
                            ANALYZING...
                        </>
                    ) : (
                        <>
                            <Play className="h-4 w-4 fill-current" />
                            RUN ANALYSIS
                        </>
                    )}
                </button>

                <div className="flex items-center gap-2 border-l border-gray-200 pl-4">
                    {/* DEV/LIVE Mode Indicator */}
                    {isUsingRealApi() ? (
                        <div className="flex items-center gap-1.5 px-3 py-1 bg-red-50 text-red-700 rounded-full border border-red-200 text-xs font-bold">
                            <Radio className="h-3 w-3" />
                            LIVE API
                        </div>
                    ) : (
                        <div className="flex items-center gap-1.5 px-3 py-1 bg-amber-50 text-amber-700 rounded-full border border-amber-200 text-xs font-bold">
                            <FlaskConical className="h-3 w-3" />
                            DEV MODE
                        </div>
                    )}
                    {/* Connection Status */}
                    <div className="flex items-center gap-1.5 px-3 py-1 bg-green-50 text-green-700 rounded-full border border-green-200 text-xs font-bold">
                        <Globe className="h-3 w-3" />
                        ONLINE
                    </div>
                </div>
            </div>
        </div>
    );
};
