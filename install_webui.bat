@echo off
REM Install Web UI dependencies for Chatterbox Dialogue Generator

echo ============================================================
echo Chatterbox Dialogue Generator - Web UI Installation
echo ============================================================
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js is not installed!
    echo.
    echo Please install Node.js 18 or later from:
    echo https://nodejs.org/
    echo.
    pause
    exit /b 1
)

echo [*] Node.js version:
node --version
echo.

REM Check if npm is installed
where npm >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] npm is not installed!
    echo npm should come with Node.js.
    pause
    exit /b 1
)

echo [*] npm version:
npm --version
echo.

REM Check if Python dependencies are installed
if not exist ".venv" (
    echo [WARNING] Python virtual environment not found!
    echo Please run install_dependencies.bat first to set up the backend.
    echo.
    echo You can still install the frontend, but you'll need the backend
    echo dependencies before you can run the web UI.
    echo.
    set /p continue="Continue anyway? (y/n): "
    if /i not "%continue%"=="y" exit /b 1
)

REM Install FastAPI dependencies if venv exists
if exist ".venv" (
    echo [*] Installing backend API dependencies...
    call .venv\Scripts\activate
    pip install fastapi==0.115.5 uvicorn[standard]==0.34.0 python-multipart==0.0.20
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to install backend dependencies!
        pause
        exit /b 1
    )
    echo [+] Backend API dependencies installed successfully!
    echo.
)

REM Install frontend dependencies
echo [*] Installing frontend dependencies...
echo This may take a few minutes...
echo.

cd apps\web

call npm install

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Failed to install frontend dependencies!
    pause
    exit /b 1
)

cd ..\..

echo.
echo ============================================================
echo Installation Complete!
echo ============================================================
echo.
echo [+] All web UI dependencies have been installed successfully!
echo.
echo To start the web UI:
echo   1. Run: start_webui.bat
echo   OR
echo   2. Start backend:  python -m apps.api.api_server
echo      Start frontend: cd apps\web ^&^& npm run dev
echo.
echo Then open your browser to: http://localhost:5173
echo.
echo See WEBUI_QUICKSTART.md for detailed instructions.
echo.
pause
