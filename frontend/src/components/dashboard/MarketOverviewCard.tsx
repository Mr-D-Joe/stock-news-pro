import React from 'react';
import type { ReviewData, AnalystRatings, RiskAssessment, MarketSentiment } from '../../types';
import { Pin, Diamond, ShieldAlert, TrendingUp, Clock } from 'lucide-react';
import { cn } from '@/lib/utils';

interface MarketOverviewCardProps {
    executiveSummary: string;
    reviewData: ReviewData;
    analystRatings: AnalystRatings;
    riskAssessment: RiskAssessment;
    marketSentiment: MarketSentiment;
    businessContext: string;
    generatedAt: string;
}

export const MarketOverviewCard: React.FC<MarketOverviewCardProps> = ({
    executiveSummary,
    reviewData,
    analystRatings,
    riskAssessment,
    marketSentiment,
    businessContext,
    generatedAt
}) => {
    return (
        <div className="w-full flex flex-col gap-6">

            {/* Executive Summary Section */}
            <div className="bg-blue-50 border-l-4 border-blue-600 p-6 rounded-r-lg shadow-sm">
                <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-2">
                        <Pin className="h-5 w-5 text-red-700 fill-red-700" />
                        <h3 className="text-lg font-bold text-slate-800">Executive Summary</h3>
                    </div>
                    {/* Timestamp */}
                    <div className="flex items-center gap-1 text-xs text-blue-600/70 font-mono">
                        <Clock className="h-3 w-3" />
                        {new Date(generatedAt).toLocaleTimeString()}
                    </div>
                </div>
                <p className="text-slate-800 text-base leading-relaxed">
                    {executiveSummary}
                </p>
            </div>

            {/* Quality & Valuation Metrics + Analyst Targets Container */}
            <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">

                <div className="flex items-center gap-2 mb-6">
                    <Diamond className="h-5 w-5 text-blue-400 fill-blue-400" />
                    <h3 className="text-lg font-bold text-slate-800">Quality & Valuation Metrics (Buffett/Lynch Style)</h3>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                    <div className="bg-white border border-gray-200 rounded-lg p-4 flex flex-col items-center justify-center shadow-sm">
                        <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-1">P/E RATIO</span>
                        <span className="text-xl font-extrabold text-slate-800">{reviewData.peRatio.toFixed(2)}</span>
                    </div>
                    <div className="bg-white border border-gray-200 rounded-lg p-4 flex flex-col items-center justify-center shadow-sm">
                        <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-1">PEG RATIO</span>
                        <span className="text-xl font-extrabold text-slate-800">{reviewData.pegRatio.toFixed(2)}</span>
                    </div>
                    <div className="bg-white border border-gray-200 rounded-lg p-4 flex flex-col items-center justify-center shadow-sm">
                        <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-1">ROE</span>
                        <span className="text-xl font-extrabold text-slate-800">{reviewData.roe.toFixed(1)}%</span>
                    </div>
                    <div className="bg-white border border-gray-200 rounded-lg p-4 flex flex-col items-center justify-center shadow-sm">
                        <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-1">DEBT/EQUITY</span>
                        <span className="text-xl font-extrabold text-slate-800">{reviewData.debtToEquity.toFixed(3)}</span>
                    </div>
                </div>

                <div className="border-t-2 border-dashed border-slate-100 my-8"></div>

                {/* Analyst Targets */}
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-8 text-center mb-8">
                    <div>
                        <div className="text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-2">TARGET (MEAN)</div>
                        <div className="text-2xl font-bold text-slate-800">${analystRatings.mean.toFixed(2)}</div>
                    </div>
                    <div>
                        <div className="text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-2">HIGH</div>
                        <div className="text-2xl font-bold text-green-700">${analystRatings.high.toFixed(2)}</div>
                    </div>
                    <div>
                        <div className="text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-2">LOW</div>
                        <div className="text-2xl font-bold text-red-700">${analystRatings.low.toFixed(2)}</div>
                    </div>
                </div>

                {/* Risk & Sentiment Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-8 pt-6 border-t border-gray-100">
                    {/* Risk */}
                    <div className="flex items-start gap-3 p-4 bg-orange-50/50 rounded-lg border border-orange-100">
                        <ShieldAlert className={cn("h-5 w-5 mt-0.5",
                            riskAssessment.level === 'High' ? "text-red-500" :
                                riskAssessment.level === 'Medium' ? "text-orange-500" : "text-green-500"
                        )} />
                        <div>
                            <div className="text-xs font-bold text-slate-500 uppercase mb-1">RISK LEVEL: {riskAssessment.level}</div>
                            <p className="text-sm text-slate-700 leading-snug">{riskAssessment.description}</p>
                        </div>
                    </div>

                    {/* AI Impact Classification (Previously Sentiment) */}
                    <div className="flex items-start gap-3 p-4 bg-purple-50/50 rounded-lg border border-purple-100">
                        <TrendingUp className="h-5 w-5 text-purple-600 mt-0.5" />
                        <div>
                            <div className="text-xs font-bold text-slate-500 uppercase mb-1">AI IMPACT CLASSIFICATION: {marketSentiment.trend} ({marketSentiment.score})</div>
                            <div className="h-1.5 w-full bg-slate-200 rounded-full mt-1 overflow-hidden">
                                <div
                                    className="h-full bg-purple-500 transition-all duration-500"
                                    style={{ width: `${marketSentiment.score}%` }}
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Business Context Footer */}
            <div className="bg-slate-50/50 p-4 border border-slate-100 rounded-lg">
                <p className="text-sm text-slate-600 leading-relaxed">
                    <span className="font-bold text-slate-800">Business Context: </span>
                    {businessContext}
                </p>
            </div>
        </div>
    );
};
