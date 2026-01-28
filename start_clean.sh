#!/bin/bash

# =============================================================================
# Stock News Pro - Clean Startup Script
# =============================================================================
# Purpose: Ensures a clean environment by freeing ports before starting the app.
# Ports Managed: 
#   - 5200 (Frontend/Tauri)
#   - 8200 (Backend/Python) - ISOLATED PORT
# =============================================================================

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}>>> Stock News Pro: Initializing clean startup...${NC}"

# Function to kill process on a port
cleanup_port() {
    local PORT=$1
    local NAME=$2
    
    # Check if port is in use
    PID=$(lsof -ti:$PORT)
    
    if [ ! -z "$PID" ]; then
        echo -e "${RED}xxx Port $PORT ($NAME) is busy (PID: $PID). Killing...${NC}"
        kill -9 $PID
        sleep 1
    else
        echo -e "${GREEN}✓ Port $PORT ($NAME) is clear.${NC}"
    fi
}

# 1. Cleanup Ports
cleanup_port 5200 "Frontend"
cleanup_port 8200 "Backend"

# 2. Clear Caches (Optional but recommended for strict clean)
echo -e "${YELLOW}>>> Cleaning temporary caches...${NC}"
rm -rf frontend/node_modules/.vite
rm -rf frontend/dist

# 3. Start Application
echo -e "${GREEN}>>> All systems clear. Launching Application on Ports 5200 / 8200...${NC}"
echo -e "${YELLOW}>>> Press Ctrl+C to quit. Cleanup will run automatically on exit.${NC}"
echo ""

cd frontend
npm run tauri dev

# 4. Final Cleanup on Exit
echo ""
echo -e "${YELLOW}>>> Shutdown detected. Ensuring cleanup...${NC}"
# Re-run cleanup just in case
cleanup_port 5200 "Frontend"
cleanup_port 8200 "Backend"
echo -e "${GREEN}>>> Shutdown complete. Goodbye!${NC}"
