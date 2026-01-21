import React from 'react';
import type { StatusBarProps } from '../types';

export const StatusBar: React.FC<StatusBarProps> = ({ statusMessage, versionInfo }) => {
    return (
        <div className="w-full bg-slate-50 border-t border-slate-200 px-6 py-2 flex items-center justify-between text-xs text-slate-500">
            <div className="flex items-center gap-2">
                <span className="h-1.5 w-1.5 bg-slate-400 rounded-full"></span>
                {statusMessage}
            </div>
            <div className="opacity-75 font-mono">
                {versionInfo}
            </div>
        </div>
    );
};
