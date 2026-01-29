import React from 'react';
import type { DataOrigin, SanitizationTrace } from '../types';
import { ShieldCheck, Database } from 'lucide-react';

interface DataOriginBadgeProps {
    dataOrigin: DataOrigin;
    sanitization: SanitizationTrace;
}

export const DataOriginBadge: React.FC<DataOriginBadgeProps> = ({ dataOrigin, sanitization }) => {
    const isLive = dataOrigin === 'live';
    return (
        <div className="flex items-center gap-2 text-[10px] font-bold">
            <span className={`px-2 py-0.5 rounded-full border uppercase tracking-wider ${isLive
                ? 'bg-red-50 text-red-700 border-red-200'
                : 'bg-amber-50 text-amber-700 border-amber-200'
                }`}>
                {isLive ? 'Live Data' : 'Mock Data'}
            </span>
            <span className="flex items-center gap-1 text-slate-500 font-mono">
                <ShieldCheck className="h-3 w-3" />
                SAN {sanitization.version}
            </span>
            <span className="flex items-center gap-1 text-slate-400 font-mono">
                <Database className="h-3 w-3" />
                {sanitization.status.toUpperCase()}
            </span>
        </div>
    );
};
