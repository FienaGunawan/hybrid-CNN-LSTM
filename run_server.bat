@echo off
REM Stock Price Prediction System - Startup Script
echo.
echo ============================================================
echo.  STOCK PRICE PREDICTION SYSTEM
echo.  Starting Flask Server...
echo.
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

REM Check if requirements are installed
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo Installing required packages...
    echo.
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install requirements
        pause
        exit /b 1
    )
)

REM Start the Flask server
echo.
echo Starting Flask server on http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python backend.py

pause
