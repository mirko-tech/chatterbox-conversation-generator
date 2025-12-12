#!/bin/bash

# Install Web UI dependencies for Chatterbox Dialogue Generator

echo "============================================================"
echo "Chatterbox Dialogue Generator - Web UI Installation"
echo "============================================================"
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "[ERROR] Node.js is not installed!"
    echo ""
    echo "Please install Node.js 18 or later from:"
    echo "https://nodejs.org/"
    echo ""
    exit 1
fi

echo "[*] Node.js version:"
node --version
echo ""

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "[ERROR] npm is not installed!"
    echo "npm should come with Node.js."
    exit 1
fi

echo "[*] npm version:"
npm --version
echo ""

# Check if Python dependencies are installed
if [ ! -d ".venv" ]; then
    echo "[WARNING] Python virtual environment not found!"
    echo "Please run ./install_dependencies.sh first to set up the backend."
    echo ""
    echo "You can still install the frontend, but you'll need the backend"
    echo "dependencies before you can run the web UI."
    echo ""
    read -p "Continue anyway? (y/n): " continue
    if [ "$continue" != "y" ] && [ "$continue" != "Y" ]; then
        exit 1
    fi
fi

# Install FastAPI dependencies if venv exists
if [ -d ".venv" ]; then
    echo "[*] Installing backend API dependencies..."
    source .venv/bin/activate
    pip install fastapi==0.115.5 uvicorn[standard]==0.34.0 python-multipart==0.0.20

    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to install backend dependencies!"
        exit 1
    fi

    echo "[+] Backend API dependencies installed successfully!"
    echo ""
fi

# Install frontend dependencies
echo "[*] Installing frontend dependencies..."
echo "This may take a few minutes..."
echo ""

cd apps/web

npm install

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Failed to install frontend dependencies!"
    exit 1
fi

cd ../..

echo ""
echo "============================================================"
echo "Installation Complete!"
echo "============================================================"
echo ""
echo "[+] All web UI dependencies have been installed successfully!"
echo ""
echo "To start the web UI:"
echo "  1. Run: ./start_webui.sh"
echo "  OR"
echo "  2. Start backend:  python -m apps.api.api_server"
echo "     Start frontend: cd apps/web && npm run dev"
echo ""
echo "Then open your browser to: http://localhost:5173"
echo ""
echo "See WEBUI_QUICKSTART.md for detailed instructions."
echo ""
