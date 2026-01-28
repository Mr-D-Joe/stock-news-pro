import React from 'react';
import { Search, TrendingUp, Zap, BarChart3, Globe } from 'lucide-react';
import { useAppContext } from '../../context/AppContext';
import { useRunAnalysisMutation } from '../../hooks/useDataFetching';

export const DashboardHero: React.FC = () => {
    const {
        setSelectedStock,
        setAnalysisStatus,
        setAnalysisResult,
        uiState
    } = useAppContext();
    const analysisMutation = useRunAnalysisMutation();

    const handleQuickAction = (ticker: string) => {
        // Pre-select and run
        setSelectedStock(ticker);
        setAnalysisStatus('loading');

        analysisMutation.mutate(
            { ticker, sector: 'General', language: uiState.selectedLanguage },
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
    };

    const TRENDING = [
        { sym: 'NVO', name: 'Novo Nordisk', gain: '+1.2%', reason: 'Obesity Market Leader' },
        { sym: 'LLY', name: 'Eli Lilly', gain: '+2.4%', reason: 'Alzheimer Drug Approval' },
        { sym: 'ACME', name: 'ACME Corp', gain: '+5.1%', reason: 'Defense Contract Win' },
    ];

    return (
        <div className="flex flex-col items-center justify-center min-h-[70vh] w-full max-w-5xl mx-auto px-4 animate-in fade-in slide-in-from-bottom-4 duration-700">

            {/* 1. HERO HEADER */}
            <div className="text-center space-y-6 mb-16 relative">
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[300px] bg-blue-400/10 blur-[100px] rounded-full pointer-events-none" />

                <h1 className="text-6xl font-black text-slate-900 tracking-tighter relative z-10">
                    Market <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-emerald-600">Intelligence</span>
                </h1>
                <p className="text-xl text-slate-500 max-w-2xl mx-auto font-light leading-relaxed relative z-10">
                    Real-time AI analysis of global markets.
                    Merging quantitative data with deep-web narrative sensing.
                </p>
            </div>

            {/* 2. ACTION CARDS */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full mb-12 relative z-10">
                {TRENDING.map((item) => (
                    <button
                        key={item.sym}
                        onClick={() => handleQuickAction(item.sym)}
                        className="group relative bg-white p-6 rounded-2xl shadow-sm hover:shadow-xl border border-slate-100 hover:border-blue-100 transition-all duration-300 text-left hover:-translate-y-1"
                    >
                        <div className="flex justify-between items-start mb-4">
                            <div className="w-10 h-10 rounded-full bg-slate-50 flex items-center justify-center group-hover:bg-blue-50 transition-colors">
                                <TrendingUp className="h-5 w-5 text-slate-400 group-hover:text-blue-600" />
                            </div>
                            <span className="text-xs font-bold px-2 py-1 bg-emerald-50 text-emerald-700 rounded-full">
                                {item.gain}
                            </span>
                        </div>

                        <h3 className="text-lg font-bold text-slate-900 mb-1 flex items-center gap-2">
                            {item.sym}
                            <span className="text-sm font-normal text-slate-400">/ {item.name}</span>
                        </h3>
                        <p className="text-sm text-slate-500 font-medium">
                            {item.reason}
                        </p>

                        <div className="absolute inset-0 border-2 border-blue-500/0 rounded-2xl group-hover:border-blue-500/5 transition-all duration-300" />
                    </button>
                ))}
            </div>

            {/* 3. CAPABILITIES GRID */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 w-full opacity-60 grayscale hover:grayscale-0 transition-all duration-500">
                {[
                    { icon: Globe, label: "Global Coverage", sub: "50,000+ Tickers" },
                    { icon: Zap, label: "Real-time AI", sub: "Gemini 2.0 Flash" },
                    { icon: BarChart3, label: "Deep Data", sub: "Institutional Grade" },
                    { icon: Search, label: "Deep Web", sub: "Sentiment Analysis" }
                ].map((feat, i) => (
                    <div key={i} className="flex flex-col items-center p-4 rounded-xl border border-transparent hover:bg-white hover:shadow-sm hover:border-slate-100 transition-all cursor-default">
                        <feat.icon className="h-6 w-6 text-slate-400 mb-2" />
                        <span className="text-sm font-bold text-slate-700">{feat.label}</span>
                        <span className="text-xs text-slate-400">{feat.sub}</span>
                    </div>
                ))}
            </div>

        </div>
    );
};
