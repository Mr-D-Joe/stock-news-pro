import { invoke } from '@tauri-apps/api/core';

// Design Goal: Encapsulate all Backend Lifecycle Logic here.
// Adheres to TA-REQ-IPC-01 (Typed IPC) and TA-REQ-START-02 (Health Check).

export const BackendService = {
    /**
     * Start the backend process via Tauri Command.
     * Only necessary if auto-start failed or was manual.
     */
    async start(): Promise<string> {
        try {
            return await invoke<string>('start_backend');
        } catch (error) {
            console.error('Failed to start backend:', error);
            throw new Error(String(error));
        }
    },

    /**
     * Stop the backend process via Tauri Command.
     */
    async stop(): Promise<string> {
        try {
            return await invoke<string>('stop_backend');
        } catch (error) {
            console.error('Failed to stop backend:', error);
            throw new Error(String(error));
        }
    },

    /**
     * Check if the backend process is running (PID check).
     */
    async isRunning(): Promise<boolean> {
        try {
            return await invoke<boolean>('backend_status');
        } catch (error) {
            console.error('Failed to check backend status:', error);
            return false;
        }
    },

    /**
     * Check if the backend is responsive via HTTP (Health Check).
     * polling logic should be handled by the caller or a hook.
     */
    async checkHealth(): Promise<boolean> {
        try {
            return await invoke<boolean>('check_backend_health');
        } catch (error) {
            // If IPC fails, assume unhealthy
            return false;
        }
    },

    /**
     * Initialize and wait for backend.
     * Retries health check for up to `timeoutMs`.
     */
    async init(timeoutMs = 10000): Promise<boolean> {
        const startTime = Date.now();

        // 1. Check if running
        const running = await this.isRunning();
        if (!running) {
            console.log("Backend not running, attempting start...");
            await this.start();
        }

        // 2. Poll for Health
        while (Date.now() - startTime < timeoutMs) {
            const healthy = await this.checkHealth();
            if (healthy) {
                console.log("Backend connection established.");
                return true;
            }
            // Wait 500ms
            await new Promise(r => setTimeout(r, 500));
        }

        console.error("Backend initialization timed out.");
        return false;
    }
};
