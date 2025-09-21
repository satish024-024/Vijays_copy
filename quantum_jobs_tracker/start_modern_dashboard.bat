@echo off
echo ============================================================
echo QUANTUM SPARK - MODERN DASHBOARD
echo ============================================================
echo Starting Quantum Jobs Tracker with Modern Dashboard...
echo.

cd /d "%~dp0"

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

echo Python found! Starting modern dashboard...
echo.

python start_modern_dashboard.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start modern dashboard
    echo Please check the error messages above
    pause
    exit /b 1
)

echo.
echo Modern dashboard stopped
pause
