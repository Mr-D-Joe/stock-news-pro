/**
 * EssayCard - Deep Dive Analysis Display
 * 
 * Uses MarkdownRenderer for rich text formatting of AI-generated essays.
 */

import React from 'react';
import { BookOpen, Sparkles } from 'lucide-react';
import { MarkdownRenderer } from '../MarkdownRenderer';

interface EssayCardProps {
    text: string;
}

export const EssayCard: React.FC<EssayCardProps> = ({ text }) => {
    return (
        <div className="w-full bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden flex flex-col">
            {/* Header */}
            <div className="bg-gradient-to-r from-slate-50 to-blue-50 px-6 py-4 border-b border-slate-200 flex items-center justify-between">
                <div className="flex items-center gap-3">
                    <div className="p-2 bg-blue-100 rounded-lg">
                        <BookOpen className="h-5 w-5 text-blue-700" />
                    </div>
                    <div>
                        <h3 className="font-bold text-slate-900">Deep Dive Essay</h3>
                        <p className="text-xs text-slate-500">AI-synthesized market analysis</p>
                    </div>
                </div>
                <div className="flex items-center gap-1 text-xs text-purple-600 bg-purple-50 px-2 py-1 rounded-full">
                    <Sparkles className="h-3 w-3" />
                    <span className="font-medium">AI GENERATED</span>
                </div>
            </div>

            {/* Body - Markdown Rendered */}
            <div className="p-6 overflow-y-auto max-h-[600px] custom-scrollbar">
                <MarkdownRenderer
                    content={text}
                    variant="essay"
                />
            </div>
        </div>
    );
};
