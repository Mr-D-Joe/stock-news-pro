import React from 'react';
import { BookOpen } from 'lucide-react';


interface EssayCardProps {
    text: string;
}

export const EssayCard: React.FC<EssayCardProps> = ({ text }) => {
    // Simple markdown parser simulation for demo if no library
    // In real app, we'd use react-markdown
    const sections = text.split('##');

    return (
        <div className="w-full max-w-[820px] bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden flex flex-col">
            <div className="bg-slate-50 px-6 py-4 border-b border-slate-200 flex items-center gap-2">
                <BookOpen className="h-5 w-5 text-gray-700" />
                <h3 className="font-bold text-gray-800">Deep Dive Essay</h3>
            </div>

            <div className="p-6 text-sm text-gray-600 leading-7 space-y-4">
                {/* Render pre-processed simple markdown-like text */}
                {sections.map((section, idx) => {
                    if (!section.trim()) return null;
                    const lines = section.trim().split('\n');
                    const title = lines[0];
                    const body = lines.slice(1).join('\n');

                    return (
                        <div key={idx} className="mb-4">
                            <h4 className="text-gray-900 font-bold text-base mb-2">{title}</h4>
                            <div className="whitespace-pre-line">{body}</div>
                        </div>
                    )
                })}
            </div>
        </div>
    );
};
