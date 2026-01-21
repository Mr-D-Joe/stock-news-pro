import React from 'react';
import type { NewsItem } from '../../types';
import { Newspaper } from 'lucide-react';

interface NewsTickerProps {
    news: NewsItem[];
    label?: string;
}

export const NewsTicker: React.FC<NewsTickerProps> = ({ news, label = "LIVE FEED" }) => {
    return (
        <div className="w-full bg-inherit text-inherit h-10 flex items-center overflow-hidden relative">
            <div className="bg-blue-600 h-full px-4 flex items-center z-10 shadow-md whitespace-nowrap">
                <Newspaper className="h-4 w-4 mr-2" />
                <span className="text-xs font-bold tracking-wider uppercase">{label}</span>
            </div>
            <div className="flex animate-marquee whitespace-nowrap gap-12 px-4 items-center">
                {news.map((item, idx) => (
                    <div key={idx} className="flex items-center gap-2">
                        <span className="text-xs font-semibold text-blue-300">[{item.timestamp}]</span>
                        <span className="text-xs font-medium">{item.title}</span>
                        <span className="text-[10px] bg-slate-800 px-2 py-0.5 rounded text-gray-400 border border-slate-700">{item.source}</span>
                    </div>
                ))}
                {/* Duplicate for infinite loop illusion if list is short */}
                {news.map((item, idx) => (
                    <div key={`d-${idx}`} className="flex items-center gap-2">
                        <span className="text-xs font-semibold text-blue-300">[{item.timestamp}]</span>
                        <span className="text-xs font-medium">{item.title}</span>
                        <span className="text-[10px] bg-slate-800 px-2 py-0.5 rounded text-gray-400 border border-slate-700">{item.source}</span>
                    </div>
                ))}
            </div>
        </div>
    );
};
