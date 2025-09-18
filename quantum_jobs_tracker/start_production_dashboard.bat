@echo off
echo 🚀 Starting Quantum Nexus Production Dashboard...
echo ================================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Start the production dashboard
echo 🔧 Launching production dashboard...
python launch_production_dashboard.py

pause
