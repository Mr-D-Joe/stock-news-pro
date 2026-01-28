/**
 * Backend Management Module
 * 
 * Per DESIGN.md Line 205-208:
 * - All Tauri commands MUST be wrapped in a typed service layer
 * - Never invoke Tauri commands directly inside React components
 * 
 * This module manages the Python backend lifecycle:
 * - Starts uvicorn server on app launch
 * - Stops server on app close
 * - Provides health check endpoint
 */

use std::process::{Child, Command};
use std::sync::Mutex;
use tauri::State;

/// Global backend process handle
pub struct BackendState(pub Mutex<Option<Child>>);

impl BackendState {
    pub fn start(&self) -> Result<String, String> {
        let mut backend = self.0.lock().map_err(|e| e.to_string())?;
        
        if backend.is_some() {
            return Ok("Backend already running".to_string());
        }
        
        let python_cmd = if cfg!(target_os = "windows") { "python" } else { "python3" };
        
        // Start uvicorn server
        let child = Command::new(python_cmd)
            .args(["-m", "uvicorn", "ai_service.main:app", "--host", "127.0.0.1", "--port", "8000"])
            .current_dir("../../")
            .spawn()
            .map_err(|e| format!("Failed to start backend: {}", e))?;
        
        let pid = child.id();
        *backend = Some(child);
        
        log::info!("Backend started with PID: {}", pid);
        Ok(format!("Backend started with PID: {}", pid))
    }

    pub fn stop(&self) -> Result<String, String> {
        let mut backend = self.0.lock().map_err(|e| e.to_string())?;
        
        if let Some(mut child) = backend.take() {
            child.kill().map_err(|e| format!("Failed to kill backend: {}", e))?;
            log::info!("Backend stopped");
            Ok("Backend stopped".to_string())
        } else {
            Ok("Backend was not running".to_string())
        }
    }
}

/// Start the Python backend server
#[tauri::command]
pub fn start_backend(state: State<BackendState>) -> Result<String, String> {
    state.start()
}

/// Stop the Python backend server
#[tauri::command]
pub fn stop_backend(state: State<BackendState>) -> Result<String, String> {
    state.stop()
}

/// Check if backend is running
#[tauri::command]
pub fn backend_status(state: State<BackendState>) -> Result<bool, String> {
    let backend = state.0.lock().map_err(|e| e.to_string())?;
    Ok(backend.is_some())
}

/// Check backend health via HTTP
#[tauri::command]
pub async fn check_backend_health() -> Result<bool, String> {
    let client = reqwest::Client::new();
    match client.get("http://127.0.0.1:8000/").send().await {
        Ok(resp) => Ok(resp.status().is_success()),
        Err(_) => Ok(false),
    }
}
