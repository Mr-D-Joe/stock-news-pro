import React from 'react';
import { Treemap, ResponsiveContainer, Tooltip } from 'recharts';
import { useSectorPerformance } from '../../hooks/useDataFetching';
import { useAppContext } from '../../context/AppContext';
import { LayoutGrid, Loader2, AlertCircle } from 'lucide-react';
import { cn } from '@/lib/utils';

// Helper to get color based on performance
const getPerformanceColor = (performance: number) => {
    // Premium color palette
    // Negative: Shades of Rose/Red
    // Neutral: Shale/Slate
    // Positive: Emerald/Green

    if (performance <= -3) return '#881337'; // rose-900
    if (performance <= -1.5) return '#be123c'; // rose-700
    if (performance < 0) return '#fb7185'; // rose-400
    if (performance === 0) return '#94a3b8'; // slate-400
    if (performance <= 1.5) return '#34d399'; // emerald-400
    if (performance <= 3) return '#059669'; // emerald-600
    return '#064e3b'; // emerald-950
};

const CustomizedContent = (props: any) => {
    const { x, y, width, height, name, performance, depth } = props;

    // Safety: Ensure performance is a number, default to 0
    const perfValue = typeof performance === 'number' ? performance : 0;
    const hasPerf = typeof performance === 'number';

    return (
        <g>
            <rect
                x={x}
                y={y}
                width={width}
                height={height}
                style={{
                    fill: getPerformanceColor(perfValue),
                    stroke: '#fff',
                    strokeWidth: 2 / (depth + 1),
                    strokeOpacity: 1 / (depth + 1),
                }}
                className="cursor-pointer hover:opacity-90 transition-opacity"
            />
            {width > 50 && height > 30 && (
                <text
                    x={x + width / 2}
                    y={y + height / 2 - 7}
                    textAnchor="middle"
                    fill="#fff"
                    fontSize={Math.min(width / 7, 14)}
                    fontWeight="bold"
                    className="pointer-events-none select-none"
                >
                    {name}
                </text>
            )}
            {width > 50 && height > 30 && hasPerf && (
                <text
                    x={x + width / 2}
                    y={y + height / 2 + 10}
                    textAnchor="middle"
                    fill="#fff"
                    fontSize={Math.min(width / 10, 12)}
                    className="pointer-events-none select-none opacity-90"
                >
                    {perfValue > 0 ? '+' : ''}{perfValue.toFixed(2)}%
                </text>
            )}
        </g>
    );
};

export const HeatmapCard: React.FC = () => {
    const { setSelectedSector, setScope } = useAppContext();
    const { data: sectors, isLoading, isError, error } = useSectorPerformance('1d');

    const handleNodeClick = (node: any) => {
        if (node && node.id) {
            setSelectedSector(node.id);
            setScope('Sector');
            console.log(`Heatmap: Selected Sector ${node.id}`);
        }
    };

    if (isLoading) {
        return (
            <div className="w-full h-[400px] bg-white rounded-xl border border-gray-100 shadow-sm flex flex-col items-center justify-center p-8">
                <Loader2 className="h-8 w-8 text-blue-500 animate-spin mb-4" />
                <p className="text-slate-500 font-medium">Loading Market Heatmap...</p>
            </div>
        );
    }

    if (isError) {
        return (
            <div className="w-full h-[400px] bg-white rounded-xl border border-gray-100 shadow-sm flex flex-col items-center justify-center p-8">
                <AlertCircle className="h-8 w-8 text-red-500 mb-4" />
                <p className="text-red-600 font-medium text-center">
                    Failed to load heatmap data<br />
                    <span className="text-xs text-slate-400">{(error as Error).message}</span>
                </p>
            </div>
        );
    }

    return (
        <div className="w-full bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden flex flex-col">
            <div className="p-4 border-b border-gray-100 flex items-center justify-between bg-slate-50/50">
                <div className="flex items-center gap-2">
                    <LayoutGrid className="h-5 w-5 text-blue-600" />
                    <h3 className="font-bold text-slate-800 uppercase tracking-wide text-xs">Market Sektor Heatmap</h3>
                </div>
                <div className="flex items-center gap-4 text-xs">
                    <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-amber-100 text-amber-700 border border-amber-200 uppercase tracking-tighter">
                        Mock Data
                    </span>
                    <div className="flex items-center gap-4 border-l border-gray-200 pl-4">
                        <div className="flex items-center gap-1">
                            <div className="w-2 h-2 rounded-full bg-emerald-600" />
                            <span className="text-slate-500">Gainers</span>
                        </div>
                        <div className="flex items-center gap-1">
                            <div className="w-2 h-2 rounded-full bg-rose-600" />
                            <span className="text-slate-500">Laggards</span>
                        </div>
                        <span className="text-slate-300 ml-2 hidden sm:inline">Size by MCAP</span>
                    </div>
                </div>
            </div>

            <div className="h-[450px] w-full p-2 bg-slate-50/30">
                <ResponsiveContainer width="100%" height="100%">
                    <Treemap
                        data={(sectors || []) as any}
                        dataKey="market_cap"
                        nameKey="name"
                        stroke="#fff"
                        content={<CustomizedContent />}
                        onClick={(node) => handleNodeClick(node)}
                    >
                        <Tooltip />
                    </Treemap>
                </ResponsiveContainer>
            </div>

            <div className="px-4 py-3 bg-white border-t border-gray-100 flex items-center justify-between">
                <p className="text-[10px] text-slate-400 italic">
                    Click a sector tile to focus analysis. Hover for details.
                </p>
                <div className="flex gap-1">
                    {['1D', '1W', '1M', '1Y'].map(p => (
                        <button
                            key={p}
                            className={cn(
                                "px-2 py-0.5 rounded text-[10px] font-bold border transition-colors",
                                p === '1D' ? "bg-blue-600 text-white border-blue-600" : "bg-white text-slate-500 border-gray-200 hover:bg-slate-50"
                            )}
                        >
                            {p}
                        </button>
                    ))}
                </div>
            </div>
        </div >
    );
};
