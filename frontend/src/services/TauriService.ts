/**
 * TauriService - Typed IPC Service Layer
 * 
 * Per DESIGN.md Line 205-208:
 * - All Tauri commands MUST be wrapped in a typed service layer
 * - Never invoke Tauri commands directly inside React components
 * - Direct invoke() calls inside components are forbidden
 * 
 * This service provides typed wrappers for all Tauri IPC commands.
 */

import { invoke } from '@tauri-apps/api/core';

// ==================== Backend Management ====================

/**
 * Start the Python backend server
 * Called automatically on app launch, but can be called manually
 */
export async function startBackend(): Promise<string> {
    return invoke<string>('start_backend');
}

/**
 * Stop the Python backend server
 * Called automatically on app close, but can be called manually
 */
export async function stopBackend(): Promise<string> {
    return invoke<string>('stop_backend');
}

/**
 * Check if backend process is running (process-level check)
 */
export async function getBackendStatus(): Promise<boolean> {
    return invoke<boolean>('backend_status');
}

/**
 * Check if backend is responding to HTTP requests (health check)
 */
export async function checkBackendHealth(): Promise<boolean> {
    return invoke<boolean>('check_backend_health');
}

// ==================== Composed Helpers ====================

/**
 * Wait for backend to be ready (with timeout)
 */
export async function waitForBackend(timeoutMs: number = 30000): Promise<boolean> {
    const startTime = Date.now();

    while (Date.now() - startTime < timeoutMs) {
        try {
            const healthy = await checkBackendHealth();
            if (healthy) return true;
        } catch {
            // Ignore errors during startup
        }
        await new Promise(resolve => setTimeout(resolve, 500));
    }

    return false;
}

/**
 * Restart the backend server
 */
export async function restartBackend(): Promise<string> {
    await stopBackend();
    await new Promise(resolve => setTimeout(resolve, 1000)); // Wait for process cleanup
    return startBackend();
}

// ==================== Export as Service Object ====================

export const TauriService = {
    startBackend,
    stopBackend,
    getBackendStatus,
    checkBackendHealth,
    waitForBackend,
    restartBackend,
};

export default TauriService;
