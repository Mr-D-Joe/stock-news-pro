
import React, { useState } from 'react';
import { usePortfolio } from '../hooks/usePortfolio';
import { Plus, Database } from 'lucide-react';

export const PortfolioDebug: React.FC = () => {
    const { transactions, loading, addTransaction, fetchPortfolio } = usePortfolio();
    const [ticker, setTicker] = useState("NVDA");
    const [amount, setAmount] = useState(10);
    const [price, setPrice] = useState(100.0);

    const handleAdd = async () => {
        await addTransaction({
            symbol: ticker,
            amount: Number(amount),
            price_at_purchase: Number(price),
            timestamp: new Date().toISOString(),
            type: 'buy'
        });
    };

    return (
        <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm space-y-4">
            <div className="flex items-center gap-2 border-b border-gray-100 pb-2">
                <div className="p-2 bg-purple-100 text-purple-700 rounded-lg">
                    <Database className="h-4 w-4" />
                </div>
                <h3 className="font-bold text-slate-800">Portfolio Persistence Debug (Phase B)</h3>
            </div>

            {/* Input Form */}
            <div className="flex gap-2">
                <input
                    className="border p-2 rounded w-20 text-sm"
                    value={ticker}
                    onChange={e => setTicker(e.target.value)}
                    placeholder="Ticker"
                />
                <input
                    className="border p-2 rounded w-20 text-sm"
                    type="number"
                    value={amount}
                    onChange={e => setAmount(Number(e.target.value))}
                    placeholder="Qty"
                />
                <input
                    className="border p-2 rounded w-24 text-sm"
                    type="number"
                    value={price}
                    onChange={e => setPrice(Number(e.target.value))}
                    placeholder="Price"
                />
                <button
                    onClick={handleAdd}
                    disabled={loading}
                    className="bg-purple-600 text-white p-2 rounded hover:bg-purple-700 disabled:opacity-50"
                >
                    <Plus className="h-4 w-4" />
                </button>
            </div>

            {/* List */}
            <div className="max-h-60 overflow-y-auto space-y-2">
                {transactions.map(tx => (
                    <div key={tx.id} className="flex justify-between items-center text-sm p-2 bg-slate-50 rounded">
                        <div>
                            <span className="font-bold text-slate-700">{tx.symbol}</span>
                            <span className="text-slate-500 ml-2">{tx.amount} @ ${tx.price_at_purchase}</span>
                        </div>
                        <div className="text-xs text-slate-400">
                            {tx.timestamp ? new Date(tx.timestamp).toLocaleTimeString() : ''}
                        </div>
                    </div>
                ))}
                {transactions.length === 0 && (
                    <div className="text-center text-slate-400 text-xs py-4">
                        No transactions found locally.
                    </div>
                )}
            </div>

            <button onClick={fetchPortfolio} className="text-xs text-blue-500 underline w-full text-center">
                Refresh Data
            </button>
        </div>
    );
};
