import React from 'react';
import { useSparklineData } from '../../hooks/useDataFetching';
import { Sparkline } from './Sparkline';
import { Bookmark, TrendingUp, TrendingDown, ChevronRight } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useAppContext } from '../../context/AppContext';

interface WatchlistItemProps {
    symbol: string;
    name: string;
    price: number;
    change: number;
}

const WatchlistItem: React.FC<WatchlistItemProps> = ({ symbol, name, price, change }) => {
    const { data: sparkline } = useSparklineData(symbol, '1w');
    const { setSelectedStock, setScope } = useAppContext();

    const isPositive = change >= 0;

    return (
        <div
            onClick={() => {
                setSelectedStock(symbol);
                setScope('Stock');
            }}
            className="flex items-center justify-between p-3 hover:bg-slate-50 transition-colors cursor-pointer border-b border-gray-100 last:border-0 group"
        >
            <div className="flex flex-col">
                <span className="font-bold text-slate-800 flex items-center gap-1">
                    {symbol}
                    <ChevronRight className="h-3 w-3 opacity-0 group-hover:opacity-100 transition-opacity text-blue-500" />
                </span>
                <span className="text-[10px] text-slate-500 truncate max-w-[80px]">{name}</span>
            </div>

            <div className="flex-1 px-4 flex justify-center">
                {sparkline && (
                    <Sparkline
                        data={sparkline.data}
                        width={80}
                        height={24}
                        strokeWidth={1.5}
                    />
                )}
            </div>

            <div className="flex flex-col items-end min-w-[70px]">
                <span className="font-mono font-bold text-slate-800">${price.toFixed(2)}</span>
                <div className={cn(
                    "flex items-center text-[10px] font-bold",
                    isPositive ? "text-emerald-600" : "text-rose-600"
                )}>
                    {isPositive ? <TrendingUp className="h-3 w-3 mr-0.5" /> : <TrendingDown className="h-3 w-3 mr-0.5" />}
                    {isPositive ? '+' : ''}{change.toFixed(2)}%
                </div>
            </div>
        </div>
    );
};

export const WatchlistCard: React.FC = () => {
    // Mock watchlist data - in real app would come from a database or context
    const watchlist = [
        { symbol: "ACME", name: "ACME Corp", price: 154.20, change: 2.5 },
        { symbol: "BGNX", name: "BioGenX Inc.", price: 78.30, change: -1.2 },
        { symbol: "NOVA", name: "NovaCraft Energy", price: 82.15, change: 3.4 },
        { symbol: "FINX", name: "FinanceX Holdings", price: 65.40, change: 0.8 }
    ];

    return (
        <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden flex flex-col h-full">
            <div className="p-4 border-b border-gray-100 flex items-center justify-between bg-slate-50/50">
                <div className="flex items-center gap-2">
                    <Bookmark className="h-5 w-5 text-blue-600 fill-blue-600" />
                    <h3 className="font-bold text-slate-800 uppercase tracking-wider text-xs">Watchlist / Top Movers</h3>
                </div>
                <div className="flex items-center gap-2">
                    <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-amber-100 text-amber-700 border border-amber-200 uppercase tracking-tighter">
                        Mock
                    </span>
                    <div className="text-[10px] text-slate-400 font-medium whitespace-nowrap">1W TREND</div>
                </div>
            </div>
            <div className="flex-1 overflow-y-auto">
                {watchlist.map(item => (
                    <WatchlistItem key={item.symbol} {...item} />
                ))}
            </div>
            <div className="p-3 bg-slate-50/50 border-t border-gray-100">
                <button className="w-full py-2 text-[10px] font-bold text-blue-600 hover:text-blue-700 transition-colors uppercase tracking-widest">
                    Manage Watchlist
                </button>
            </div>
        </div>
    );
};
