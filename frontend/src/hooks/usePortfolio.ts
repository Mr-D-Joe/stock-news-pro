
import { useState, useCallback, useEffect } from 'react';
import type { Transaction } from '../types';
import { ApiService } from '../services/ApiService';

export const usePortfolio = () => {
    const [transactions, setTransactions] = useState<Transaction[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const service = ApiService as {
        getPortfolio?: () => Promise<Transaction[]>;
        addTransaction?: (tx: Transaction) => Promise<Transaction>;
    };

    const fetchPortfolio = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            if (!service.getPortfolio) {
                setError("Portfolio API not available");
                return;
            }
            const data = await service.getPortfolio();
            setTransactions(data);
        } catch (err) {
            console.error(err);
            setError("Failed to fetch portfolio");
        } finally {
            setLoading(false);
        }
    }, [service]);

    const addTransaction = useCallback(async (tx: Transaction) => {
        setLoading(true);
        try {
            if (!service.addTransaction) {
                setError("Portfolio API not available");
                throw new Error("Portfolio API not available");
            }
            const newTx = await service.addTransaction(tx);
            setTransactions(prev => [newTx, ...prev]);
            return newTx;
        } catch (err) {
            console.error(err);
            setError("Failed to add transaction");
            throw err;
        } finally {
            setLoading(false);
        }
    }, [service]);

    const deleteTransaction = useCallback(async (id: number) => {
        void id;
        // Note: Delete method needs to be added to ApiService interface first if supported in Frontend Service
        // For now just local optimistic update or skip if implementation is pending in Frontend Service
        console.warn("Delete not yet fully implemented in Frontend Service interface");
    }, []);

    // Initial fetch
    useEffect(() => {
        fetchPortfolio();
    }, [fetchPortfolio]);

    return {
        transactions,
        loading,
        error,
        fetchPortfolio,
        addTransaction,
        deleteTransaction
    };
};
