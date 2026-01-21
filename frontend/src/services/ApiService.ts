/**
 * ApiService Factory
 * 
 * Returns MockApiService or RealApiService based on environment configuration.
 * Toggle via VITE_USE_REAL_API in .env
 */

import { MockApiService } from './MockApiService';
import { RealApiService } from './RealApiService';

// Check environment variable
const USE_REAL_API = import.meta.env.VITE_USE_REAL_API === 'true';

// Log which service is being used
console.log(`📡 ApiService: Using ${USE_REAL_API ? 'REAL' : 'MOCK'} backend`);

/**
 * The active API service instance
 */
export const ApiService = USE_REAL_API ? RealApiService : MockApiService;

/**
 * Check if using real API
 */
export const isUsingRealApi = () => USE_REAL_API;

/**
 * Get API base URL (only relevant for real API)
 */
export const getApiBaseUrl = () => import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export default ApiService;
