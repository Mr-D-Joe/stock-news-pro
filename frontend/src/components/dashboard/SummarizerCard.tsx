import React from 'react';
import { Sparkles } from 'lucide-react';
import type { Metric } from '../../types';

interface SummarizerCardProps {
    summary: string;
    metrics: Metric[];
}

export const SummarizerCard: React.FC<SummarizerCardProps> = ({ summary, metrics }) => {
    return (
        <div className="w-full max-w-[820px] bg-white border border-gray-200 rounded-xl shadow-sm p-6 flex flex-col gap-4">
            <div className="flex items-center justify-between pb-2 border-b border-gray-100">
                <div className="flex items-center gap-2">
                    <div className="p-1.5 bg-purple-100 rounded-md">
                        <Sparkles className="h-4 w-4 text-purple-600" />
                    </div>
                    <h3 className="font-bold text-gray-900">AI Summary</h3>
                </div>
                <div className="text-[10px] text-gray-400 font-mono">MODEL: GEMINI-PRO</div>
            </div>

            <p className="text-sm text-gray-700 leading-relaxed font-normal">
                {summary}
            </p>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2">
                {metrics.map((m, i) => (
                    <div key={i} className="bg-slate-50 p-3 rounded-lg border border-slate-100 flex flex-col items-center">
                        <span className="text-[10px] uppercase font-bold text-slate-400 mb-1">{m.label}</span>
                        <span className="text-base font-bold text-slate-800">{m.value}</span>
                    </div>
                ))}
            </div>
        </div>
    );
};
