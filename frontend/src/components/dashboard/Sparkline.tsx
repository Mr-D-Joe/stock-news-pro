import React, { useMemo } from 'react';

interface SparklineProps {
    data: number[];
    width?: number;
    height?: number;
    color?: string;
    strokeWidth?: number;
    className?: string;
    /** Normalize scale across all sparklines if true */
    normalized?: boolean;
    /** Custom min/max range for normalization */
    range?: [number, number];
}

/**
 * Sparkline - Lightweight SVG mini-chart for trend visualization.
 * 
 * Implements UI-REQ-SPARK-01, UI-REQ-SPARK-02, UI-REQ-SPARK-04.
 */
export const Sparkline: React.FC<SparklineProps> = ({
    data,
    width = 120,
    height = 30,
    color,
    strokeWidth = 2,
    className = "",
    normalized = false,
    range
}) => {
    const points = useMemo(() => {
        if (!data || data.length < 2) return "";

        const min = range?.[0] ?? (normalized ? Math.min(...data) : Math.min(...data));
        const max = range?.[1] ?? (normalized ? Math.max(...data) : Math.max(...data));
        const diff = max - min || 1;

        const xScale = width / (data.length - 1);
        const yScale = height / diff;

        return data.map((val, i) => {
            const x = i * xScale;
            const y = height - (val - min) * yScale;
            return `${x},${y}`;
        }).join(" ");
    }, [data, width, height, normalized, range]);

    const trendColor = useMemo(() => {
        if (color) return color;
        if (!data || data.length < 2) return "#94a3b8"; // slate-400

        const first = data[0];
        const last = data[data.length - 1];

        return last >= first
            ? "#10b981" // emerald-500
            : "#f43f5e"; // rose-500
    }, [data, color]);

    if (!data || data.length < 2) {
        return <div style={{ width, height }} className={`flex items-center justify-center ${className}`}>
            <div className="w-1/2 h-[1px] bg-slate-700/50" />
        </div>;
    }

    return (
        <svg
            width={width}
            height={height}
            viewBox={`0 0 ${width} ${height}`}
            className={`overflow-visible ${className}`}
        >
            <polyline
                fill="none"
                stroke={trendColor}
                strokeWidth={strokeWidth}
                strokeLinecap="round"
                strokeLinejoin="round"
                points={points}
                style={{ transition: 'all 0.3s ease' }}
            />
            {/* Gradient Area (Optional for premium feel) */}
            <defs>
                <linearGradient id={`grad-${trendColor.replace('#', '')}`} x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor={trendColor} stopOpacity="0.2" />
                    <stop offset="100%" stopColor={trendColor} stopOpacity="0" />
                </linearGradient>
            </defs>
            <path
                d={`M 0,${height} L ${points} L ${width},${height} Z`}
                fill={`url(#grad-${trendColor.replace('#', '')})`}
                style={{ transition: 'all 0.3s ease' }}
            />
        </svg>
    );
};

export default React.memo(Sparkline);
