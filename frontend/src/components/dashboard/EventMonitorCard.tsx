import React from 'react';
import type { EventMonitorCardProps } from '../../types';
import { LineChart, Line, BarChart, Bar, ResponsiveContainer, XAxis, YAxis, Tooltip } from 'recharts';
import { Zap, Clock, BarChart2 } from 'lucide-react';

import { useAppContext } from '../../context/AppContext';
import { cn } from '@/lib/utils';
import type { Timeframe } from '../../types';

export const EventMonitorCard: React.FC<EventMonitorCardProps> = ({ chartData, volumeData, sectorNews }) => {

    // Connect to Context for Timeframe Control (per DESIGN.md L119)
    const { uiState, setTimeframe } = useAppContext();
    const { selectedTimeframe: selectedPeriod } = uiState;

    // Filter Data based on global Timeframe
    const getData = () => {
        if (!chartData || chartData.length === 0) return [];
        const len = chartData.length;

        switch (selectedPeriod) {
            case '24H': return chartData.slice(len - 5);    // 1 Day (Simulated)
            case '7D': return chartData.slice(len - 7);     // 1 Week
            case '1M': return chartData.slice(len - 30);    // 1 Month
            case '3M': return chartData.slice(len - 90);    // 3 Months
            case '6M': return chartData.slice(len - 180);   // 6 Months
            case '1Y': return chartData.slice(len - 365);   // 1 Year
            case '3Y': return chartData.slice(len - 1095);  // 3 Years
            case '5Y': return chartData.slice(len - 1825);  // 5 Years
            case '10Y': return chartData.slice(len - 3650); // 10 Years
            case 'ALL': return chartData;                   // All
            default: return chartData.slice(len - 365);
        }
    };

    const finalData = getData();

    // Map Slider Integer to Timeframe Strings
    const TIMEFRAMES: Timeframe[] = ['24H', '7D', '1M', '3M', '6M', '1Y', '3Y', '5Y', '10Y', 'ALL'];
    const currentIndex = TIMEFRAMES.indexOf(selectedPeriod as Timeframe) === -1 ? 5 : TIMEFRAMES.indexOf(selectedPeriod as Timeframe);

    return (
        <div className="w-full max-w-[800px] flex flex-col gap-6 p-4 bg-white rounded-xl shadow-sm border border-gray-100">
            {/* Header */}
            <div className="flex items-center justify-between pb-2 border-b border-gray-100">
                <div className="flex items-center gap-2">
                    <Zap className="h-5 w-5 text-amber-500" />
                    <h2 className="text-lg font-bold text-gray-900">Event Monitor</h2>
                </div>
                <div className="text-xs font-bold text-blue-600 bg-blue-50 px-3 py-1 rounded-full border border-blue-100">
                    {selectedPeriod} VIEW
                </div>
            </div>

            {/* Price Chart */}
            <div className="h-64 w-full bg-slate-50/50 rounded-lg border border-slate-100 p-2 relative">
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={finalData}>
                        <XAxis dataKey="date" hide />
                        <YAxis domain={['auto', 'auto']} hide />
                        <Tooltip
                            contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}
                            labelStyle={{ color: '#64748b', fontSize: '10px' }}
                        />
                        <Line
                            type="monotone"
                            dataKey="value"
                            stroke="#2563eb"
                            strokeWidth={2}
                            dot={false}
                            activeDot={{ r: 4, fill: '#2563eb' }}
                        />
                    </LineChart>
                </ResponsiveContainer>
                <div className="absolute top-2 left-4 text-[10px] text-slate-400 font-bold uppercase tracking-wider">
                    Price Action ({selectedPeriod})
                </div>
            </div>

            {/* Volume Chart (48H Hourly) - F-UI-11 */}
            {volumeData && volumeData.length > 0 && (
                <div className="h-32 w-full bg-slate-50/50 rounded-lg border border-slate-100 p-2 relative">
                    <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={volumeData}>
                            <Tooltip
                                cursor={{ fill: '#f1f5f9' }}
                                contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}
                                labelStyle={{ color: '#64748b', fontSize: '10px' }}
                                formatter={(value: number | undefined) => [
                                    value !== undefined ? new Intl.NumberFormat('en-US', { notation: "compact" }).format(value) : '',
                                    "Volume"
                                ]}
                                labelFormatter={(label) => new Date(label).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                            />
                            <Bar dataKey="volume" fill="#cbd5e1" radius={[2, 2, 0, 0]} />
                        </BarChart>
                    </ResponsiveContainer>
                    <div className="absolute top-2 left-4 flex items-center gap-2">
                        <BarChart2 className="h-3 w-3 text-slate-400" />
                        <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">
                            Volume (48H Hourly)
                        </span>
                    </div>
                </div>
            )}

            {/* Enhanced Range Slider with Ticks */}
            <div className="px-2">
                <div className="relative h-12">
                    {/* Tick Marks Layer */}
                    <div className="absolute top-4 left-0 right-0 flex justify-between px-1">
                        {TIMEFRAMES.map((tf, idx) => (
                            <div key={tf} className="flex flex-col items-center gap-1" style={{ width: '20px' }}>
                                {/* Tick Line */}
                                <div className={cn(
                                    "w-0.5 h-2 rounded-full transition-colors",
                                    idx <= currentIndex ? "bg-blue-500" : "bg-gray-200"
                                )} />
                                {/* Label */}
                                <span className={cn(
                                    "text-[10px] font-bold transition-colors",
                                    idx === currentIndex ? "text-blue-600" : "text-gray-400"
                                )}>
                                    {tf}
                                </span>
                            </div>
                        ))}
                    </div>

                    {/* Actual Slider Input */}
                    <input
                        type="range"
                        min="0"
                        max="9"
                        step="1"
                        value={currentIndex}
                        className="absolute top-3 w-full h-2 bg-transparent appearance-none cursor-pointer z-10"
                        style={{ background: 'transparent' }} // Ensure transparency so custom ticks show? Actually standard input covers it. We need custom track.
                        // Simplified styling for now to ensure functionality first
                        onChange={(e) => {
                            const val = parseInt(e.target.value);
                            setTimeframe(TIMEFRAMES[val]);
                        }}
                    />
                    {/* Custom Track (Behind) */}
                    <div className="absolute top-4 left-0 right-0 h-1 bg-gray-100 rounded-full -z-0">
                        <div
                            className="h-full bg-blue-100 rounded-full transition-all duration-300"
                            style={{ width: `${(currentIndex / 9) * 100}%` }}
                        />
                    </div>
                </div>
            </div>

            {/* Sector News Ticker */}
            <div className="flex flex-col gap-3">
                <div className="flex items-center gap-2 text-amber-700 font-bold text-sm">
                    <Clock className="h-4 w-4" />
                    Sector News
                </div>
                <div className="bg-amber-50 border-l-4 border-amber-400 p-3 rounded-r-md h-24 overflow-y-auto custom-scrollbar">
                    <ul className="space-y-2">
                        {sectorNews.map((news, idx) => (
                            <li key={idx} className="text-xs text-amber-900 flex items-start gap-2">
                                <span className="mt-1 block h-1 w-1 bg-amber-400 rounded-full flex-shrink-0"></span>
                                {news}
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    );
};
