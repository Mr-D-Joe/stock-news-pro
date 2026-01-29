
import React from 'react';
import type { ThemeResult, ThemeAsset } from '../types';
import { TrendingUp, TrendingDown, Info, BookOpen } from 'lucide-react';
import { DataOriginBadge } from './DataOriginBadge';

interface ThematicReportProps {
    data: ThemeResult;
}

const AssetCard = ({ asset, type }: { asset: ThemeAsset; type: 'winner' | 'loser' }) => (
    <div className={`p-4 rounded-lg border flex items-start justify-between gap-4 ${type === 'winner'
        ? 'bg-green-50 border-green-200 text-green-900'
        : 'bg-red-50 border-red-200 text-red-900'
        }`}>
        <div className="flex-1">
            <div className="flex items-center gap-2 mb-1">
                <span className="font-bold text-lg">{asset.symbol}</span>
                <span className={`text-xs px-2 py-0.5 rounded-full font-bold ${type === 'winner' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                    }`}>
                    {type === 'winner' ? 'WINNER' : 'RISK'}
                </span>
            </div>
            <div className="font-semibold text-sm mb-1">{asset.name}</div>
            <div className="text-sm opacity-80">{asset.reason}</div>
        </div>
        <div>
            {type === 'winner'
                ? <TrendingUp className="h-6 w-6 text-green-600" />
                : <TrendingDown className="h-6 w-6 text-red-600" />
            }
        </div>
    </div>
);

export const ThematicReport: React.FC<ThematicReportProps> = ({ data }) => {
    return (
        <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500 pb-12">

            {/* HERDER */}
            <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
                <div className="flex items-start gap-4">
                    <div className="p-3 bg-blue-100 text-blue-700 rounded-lg">
                        <BookOpen className="h-6 w-6" />
                    </div>
                    <div>
                        <h2 className="text-2xl font-bold text-slate-900 uppercase mb-2">
                            Theme Analysis: {data.theme}
                        </h2>
                        <p className="text-slate-600 text-lg leading-relaxed">
                            {data.description}
                        </p>
                        <div className="mt-3">
                            <DataOriginBadge dataOrigin={data.dataOrigin} sanitization={data.sanitization} />
                        </div>
                    </div>
                </div>
            </div>

            {/* WINNERS / LOSERS GRID */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">

                {/* Winners Column */}
                <div className="space-y-4">
                    <h3 className="flex items-center gap-2 text-lg font-bold text-green-700 uppercase tracking-wider">
                        <TrendingUp className="h-5 w-5" />
                        Structural Winners
                    </h3>
                    <div className="grid gap-4">
                        {data.winners.map(asset => (
                            <AssetCard key={asset.symbol} asset={asset} type="winner" />
                        ))}
                        {data.winners.length === 0 && (
                            <div className="p-4 bg-gray-50 text-gray-400 italic rounded-lg">
                                No clear winners identified.
                            </div>
                        )}
                    </div>
                </div>

                {/* Losers Column */}
                <div className="space-y-4">
                    <h3 className="flex items-center gap-2 text-lg font-bold text-red-700 uppercase tracking-wider">
                        <TrendingDown className="h-5 w-5" />
                        Risks & Headwinds
                    </h3>
                    <div className="grid gap-4">
                        {data.losers.map(asset => (
                            <AssetCard key={asset.symbol} asset={asset} type="loser" />
                        ))}
                        {data.losers.length === 0 && (
                            <div className="p-4 bg-gray-50 text-gray-400 italic rounded-lg">
                                No significant risks identified.
                            </div>
                        )}
                    </div>
                </div>
            </div>

            {/* ESSAY SECTION */}
            <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
                <div className="bg-slate-50 border-b border-slate-200 px-6 py-4 flex items-center gap-2">
                    <Info className="h-4 w-4 text-slate-500" />
                    <h3 className="text-sm font-bold text-slate-700 uppercase tracking-wider">
                        Strategic Context
                    </h3>
                </div>
                <div className="p-8 prose prose-slate max-w-none">
                    <div className="whitespace-pre-wrap font-serif text-lg leading-relaxed text-slate-800">
                        {data.essay}
                    </div>
                </div>
            </div>

            <div className="text-center pt-8 text-xs text-slate-400 font-mono uppercase">
                Generated by Stock News Pro AI Engine • {new Date(data.generated_at).toLocaleString()}
            </div>
        </div>
    );
};
