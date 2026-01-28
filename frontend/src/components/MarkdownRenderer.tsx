/**
 * MarkdownRenderer - Rich Text Display Component
 * 
 * Provides styled Markdown rendering with Tailwind Typography.
 * Used for AI-generated essays, summaries, and analysis reports.
 */

import React from 'react';
import ReactMarkdown from 'react-markdown';

interface MarkdownRendererProps {
    content: string;
    className?: string;
    variant?: 'default' | 'compact' | 'essay';
}

export const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({
    content,
    className = '',
    variant = 'default'
}) => {
    const variantStyles = {
        default: 'prose prose-slate prose-sm max-w-none',
        compact: 'prose prose-slate prose-xs max-w-none prose-headings:text-sm',
        essay: 'prose prose-slate prose-base max-w-none prose-headings:font-bold prose-headings:text-slate-900 prose-p:text-slate-700 prose-p:leading-relaxed prose-li:text-slate-700 prose-strong:text-slate-900 prose-a:text-blue-600 prose-a:no-underline hover:prose-a:underline'
    };

    return (
        <div className={`${variantStyles[variant]} ${className}`}>
            <ReactMarkdown
                components={{
                    // Custom heading styles
                    h1: ({ children }) => (
                        <h1 className="text-2xl font-extrabold text-slate-900 mb-4 mt-6 first:mt-0 border-b border-slate-200 pb-2">
                            {children}
                        </h1>
                    ),
                    h2: ({ children }) => (
                        <h2 className="text-xl font-bold text-slate-800 mb-3 mt-5 first:mt-0">
                            {children}
                        </h2>
                    ),
                    h3: ({ children }) => (
                        <h3 className="text-lg font-semibold text-slate-700 mb-2 mt-4 first:mt-0">
                            {children}
                        </h3>
                    ),
                    // Paragraphs with better spacing
                    p: ({ children }) => (
                        <p className="text-slate-700 leading-relaxed mb-4 last:mb-0">
                            {children}
                        </p>
                    ),
                    // Lists
                    ul: ({ children }) => (
                        <ul className="list-disc list-inside space-y-1 mb-4 text-slate-700">
                            {children}
                        </ul>
                    ),
                    ol: ({ children }) => (
                        <ol className="list-decimal list-inside space-y-1 mb-4 text-slate-700">
                            {children}
                        </ol>
                    ),
                    li: ({ children }) => (
                        <li className="text-slate-700 pl-1">
                            {children}
                        </li>
                    ),
                    // Emphasis
                    strong: ({ children }) => (
                        <strong className="font-bold text-slate-900">
                            {children}
                        </strong>
                    ),
                    em: ({ children }) => (
                        <em className="italic text-slate-600">
                            {children}
                        </em>
                    ),
                    // Blockquotes for callouts
                    blockquote: ({ children }) => (
                        <blockquote className="border-l-4 border-blue-500 bg-blue-50 pl-4 py-2 my-4 text-slate-700 italic rounded-r-lg">
                            {children}
                        </blockquote>
                    ),
                    // Code blocks
                    code: ({ children, className }) => {
                        const isInline = !className;
                        return isInline ? (
                            <code className="bg-slate-100 text-slate-800 px-1.5 py-0.5 rounded text-sm font-mono">
                                {children}
                            </code>
                        ) : (
                            <code className="block bg-slate-900 text-slate-100 p-4 rounded-lg text-sm font-mono overflow-x-auto">
                                {children}
                            </code>
                        );
                    },
                    // Horizontal rules
                    hr: () => (
                        <hr className="border-t-2 border-slate-200 my-6" />
                    ),
                    // Links
                    a: ({ href, children }) => (
                        <a
                            href={href}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-600 hover:text-blue-800 hover:underline transition-colors"
                        >
                            {children}
                        </a>
                    ),
                }}
            >
                {content}
            </ReactMarkdown>
        </div>
    );
};
