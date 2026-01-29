
import { useState, useCallback, useEffect } from 'react';
import type { Transaction } from '../types';
import { ApiService } from '../services/ApiService';

export const usePortfolio = () => {
    const [transactions, setTransactions] = useState<Transaction[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const fetchPortfolio = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const data = await ApiService.getPortfolio();
            setTransactions(data);
        } catch (err) {
            console.error(err);
            setError("Failed to fetch portfolio");
        } finally {
            setLoading(false);
        }
    }, []);

    const addTransaction = useCallback(async (tx: Transaction) => {
        setLoading(true);
        try {
            const newTx = await ApiService.addTransaction(tx);
            setTransactions(prev => [newTx, ...prev]);
            return newTx;
        } catch (err) {
            console.error(err);
            setError("Failed to add transaction");
            throw err;
        } finally {
            setLoading(false);
        }
    }, []);

    const deleteTransaction = useCallback(async (id: number) => {
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
