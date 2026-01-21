/**
 * Tauri Application Entry Point
 * 
 * Manages:
 * - Backend lifecycle (auto-start on app launch, auto-stop on close)
 * - IPC commands for frontend-backend communication
 * - Plugin registration
 */

mod backend;

use backend::{BackendState, start_backend, stop_backend, backend_status, check_backend_health};
use std::sync::Mutex;
use tauri::Manager;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        // Register backend state
        .manage(BackendState(Mutex::new(None)))
        
        // Register IPC commands (per DESIGN.md Line 205-208)
        .invoke_handler(tauri::generate_handler![
            start_backend,
            stop_backend,
            backend_status,
            check_backend_health
        ])
        
        .setup(|app| {
            // Plugin setup
            if cfg!(debug_assertions) {
                app.handle().plugin(
                    tauri_plugin_log::Builder::default()
                        .level(log::LevelFilter::Info)
                        .build(),
                )?;
            }
            
            // Auto-start backend on app launch
            log::info!("Starting backend server...");
            let state = app.state::<BackendState>();
            match start_backend_internal(&state) {
                Ok(msg) => log::info!("{}", msg),
                Err(e) => log::error!("Failed to start backend: {}", e),
            }
            
            Ok(())
        })
        
        // Auto-stop backend on app close
        .on_window_event(|window, event| {
            if let tauri::WindowEvent::CloseRequested { .. } = event {
                log::info!("Window closing, stopping backend...");
                let state = window.state::<BackendState>();
                if let Err(e) = stop_backend_internal(&state) {
                    log::error!("Failed to stop backend: {}", e);
                }
            }
        })
        
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

/// Internal function to start backend (not a Tauri command)
fn start_backend_internal(state: &BackendState) -> Result<String, String> {
    use std::process::Command;
    
    let mut backend = state.0.lock().map_err(|e| e.to_string())?;
    
    if backend.is_some() {
        return Ok("Backend already running".to_string());
    }
    
    let python_cmd = if cfg!(target_os = "windows") { "python" } else { "python3" };
    
    let child = Command::new(python_cmd)
        .args(["-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"])
        .current_dir("../ai_service")
        .spawn()
        .map_err(|e| format!("Failed to start backend: {}", e))?;
    
    let pid = child.id();
    *backend = Some(child);
    
    Ok(format!("Backend started with PID: {}", pid))
}

/// Internal function to stop backend (not a Tauri command)
fn stop_backend_internal(state: &BackendState) -> Result<String, String> {
    let mut backend = state.0.lock().map_err(|e| e.to_string())?;
    
    if let Some(mut child) = backend.take() {
        child.kill().map_err(|e| format!("Failed to kill backend: {}", e))?;
        Ok("Backend stopped".to_string())
    } else {
        Ok("Backend was not running".to_string())
    }
}
