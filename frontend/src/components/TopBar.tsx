import React from 'react';
import { Globe, Play, Loader2, Search, Target, PieChart } from 'lucide-react';
import { useAppContext } from '../context/AppContext';
import { cn } from '@/lib/utils';
import type { AnalysisScope } from '../types';

export const TopBar: React.FC = () => {
    const {
        state,
        setStockInput,
        setSectorInput,
        setLanguageInput,
        setScope,
        runAnalysis,
        resolveStockInput,
        resolveLanguageInput
    } = useAppContext();
    const { selectedStock, selectedSector, selectedLanguage, selectedScope, analysisStatus } = state;

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
                        value={selectedStock}
                        onChange={(e) => setStockInput(e.target.value)}
                        onFocus={(e) => e.target.select()} // Select on Focus (Tab)
                        onClick={(e) => e.currentTarget.select()} // Select on Click (Mouse)
                        // Fix for selection jumping: Prevent deselect on release
                        onMouseUp={(e) => e.preventDefault()}
                        onBlur={() => resolveStockInput(selectedStock)}
                        onKeyDown={async (e) => {
                            if (e.key === 'Enter') {
                                e.currentTarget.blur();
                                const resolvedParams = await resolveStockInput(selectedStock);
                                runAnalysis(resolvedParams || selectedStock);
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
                        onChange={(e) => setSectorInput(e.target.value)}
                        onFocus={(e) => e.target.select()}
                        onClick={(e) => e.currentTarget.select()}
                        onMouseUp={(e) => e.preventDefault()}
                    />
                </div>

                {/* Language Input (New) */}
                <div className="relative w-32">
                    <div className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
                        <Globe className="h-4 w-4" />
                    </div>
                    <input
                        type="text"
                        className="w-full pl-9 pr-2 py-2 rounded-lg bg-slate-50 border border-gray-200 text-sm font-medium text-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500 placeholder:text-gray-400"
                        placeholder="LANG"
                        value={selectedLanguage}
                        onChange={(e) => setLanguageInput(e.target.value)}
                        onFocus={(e) => e.target.select()}
                        onClick={(e) => e.currentTarget.select()}
                        onMouseUp={(e) => e.preventDefault()}
                        onBlur={() => resolveLanguageInput(selectedLanguage)}
                        onKeyDown={(e) => {
                            if (e.key === 'Enter') {
                                e.currentTarget.blur();
                                resolveLanguageInput(selectedLanguage);
                            }
                        }}
                    />
                </div>



                {/* Scope Select */}
                <div className="relative w-[140px]">
                    <div className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
                        <Target className="h-4 w-4" />
                    </div>
                    <select
                        className="w-full pl-9 pr-2 py-2 rounded-lg bg-slate-50 border border-gray-200 text-sm font-medium text-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500 appearance-none cursor-pointer"
                        value={selectedScope}
                        onChange={(e) => setScope(e.target.value as AnalysisScope)}
                    >
                        <option value="Stock">Stock Only</option>
                        <option value="Sector">Sector Only</option>
                        <option value="Market">Market Only</option>
                        <option value="Combined">Combined</option>
                    </select>
                </div>
            </div>

            {/* ACTION AREA */}
            <div className="flex items-center gap-4">
                <button
                    disabled={!selectedStock || analysisStatus === 'loading'}
                    onClick={() => runAnalysis()}
                    className={cn(
                        "flex items-center gap-2 px-6 py-2 rounded-lg text-sm font-bold shadow-sm transition-all min-w-[150px] justify-center",
                        !selectedStock
                            ? "bg-gray-100 text-gray-400 cursor-not-allowed"
                            : "bg-blue-600 text-white hover:bg-blue-700 shadow-blue-200 hover:shadow-md active:translate-y-0.5"
                    )}
                >
                    {analysisStatus === 'loading' ? (
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
                    {/* Status Indicator */}
                    <div className="flex items-center gap-1.5 px-3 py-1 bg-green-50 text-green-700 rounded-full border border-green-200 text-xs font-bold">
                        <Globe className="h-3 w-3" />
                        ONLINE
                    </div>
                </div>
            </div>
        </div>
    );
};
