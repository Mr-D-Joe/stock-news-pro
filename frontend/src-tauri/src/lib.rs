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
            
            app.handle().plugin(tauri_plugin_shell::init())?;
            
            // Auto-start backend on app launch
            log::info!("Starting backend server...");
            let state = app.state::<BackendState>();
            match state.start() {
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
                if let Err(e) = state.stop() {
                    log::error!("Failed to stop backend: {}", e);
                }
            }
        })
        
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
