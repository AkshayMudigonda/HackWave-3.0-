@echo off
title AI Assistant Launcher

echo ==========================================================
echo   AI Assistant — Full Stack Launcher
echo ==========================================================
echo.

REM --- Check Python is available ---
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python was not found. Please install Python 3.10+ and try again.
    pause
    exit /b 1
)

REM --- Check Node / npm is available ---
where npm >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] npm was not found. Please install Node.js and try again.
    pause
    exit /b 1
)

REM --- Install frontend dependencies if node_modules is missing ---
if not exist "%~dp0frontend\node_modules" (
    echo [Setup] Installing frontend dependencies ...
    pushd "%~dp0frontend"
    npm install
    popd
)

REM --- Install backend Python dependencies ---
echo [Setup] Installing backend Python dependencies ...
pip install -q -r "%~dp0backend\Assistant\requirements.txt"

echo.
echo [1/2] Starting backend API server (port 8000) ...
echo       The browser will open automatically once the server is ready.
echo.

REM --- Start the backend in a new terminal window ---
start "Assistant Backend" cmd /k "cd /d "%~dp0backend\Assistant" && python main.py --serve"

REM --- Give the backend a moment to start before npm run dev ---
timeout /t 2 /nobreak >nul

echo [2/2] Starting frontend dev server (port 5173) ...
echo.

REM --- Start the frontend in a new terminal window ---
start "Assistant Frontend" cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo.
echo ==========================================================
echo   Both servers are starting in separate windows.
echo   Backend  : http://localhost:8000
echo   Frontend : http://localhost:5173  (opens automatically)
echo ==========================================================
echo.
echo   Close this window or press Ctrl+C in either server
echo   window to stop the respective service.
echo.
pause
