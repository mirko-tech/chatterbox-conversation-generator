@echo off
REM Start both backend and frontend for Chatterbox Dialogue Generator Web UI

echo ============================================================
echo Chatterbox Dialogue Generator - Web UI Launcher
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo [ERROR] Virtual environment not found!
    echo Please run install_dependencies.bat first.
    pause
    exit /b 1
)

REM Check if web node_modules exists
if not exist "apps\web\node_modules" (
    echo [*] Installing frontend dependencies...
    cd apps\web
    call npm install
    cd ..\..
)

echo [*] Starting backend API server...
echo [*] API will be available at: http://localhost:8000
echo.

REM Start backend in new window
start "Chatterbox API Server" cmd /k ".venv\Scripts\activate && python -m apps.api.api_server"

REM Wait a moment for backend to start
timeout /t 3 /nobreak > nul

echo [*] Starting frontend development server...
echo [*] Web UI will be available at: http://localhost:5173
echo.

REM Start frontend in new window
start "Chatterbox Web UI" cmd /k "cd apps\web && npm run dev"

echo.
echo [+] Both servers are starting in separate windows.
echo [+] Close those windows to stop the servers.
echo.
pause
