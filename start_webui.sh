#!/bin/bash

# Start both backend and frontend for Chatterbox Dialogue Generator Web UI

echo "============================================================"
echo "Chatterbox Dialogue Generator - Web UI Launcher"
echo "============================================================"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "[ERROR] Virtual environment not found!"
    echo "Please run ./install_dependencies.sh first."
    exit 1
fi

# Check if web node_modules exists
if [ ! -d "apps/web/node_modules" ]; then
    echo "[*] Installing frontend dependencies..."
    cd apps/web
    npm install
    cd ../..
fi

# Activate virtual environment
source .venv/bin/activate

echo "[*] Starting backend API server..."
echo "[*] API will be available at: http://localhost:8000"
echo ""

# Start backend in background
python -m apps.api.api_server &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

echo "[*] Starting frontend development server..."
echo "[*] Web UI will be available at: http://localhost:5173"
echo ""

# Start frontend
cd apps/web
npm run dev &
FRONTEND_PID=$!

# Trap Ctrl+C and cleanup
trap "echo ''; echo '[*] Shutting down servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM

echo ""
echo "[+] Both servers are running."
echo "[+] Press Ctrl+C to stop both servers."
echo ""

# Wait for both processes
wait
