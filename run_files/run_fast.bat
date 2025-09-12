@echo off
echo ⚡ Fast Quantum Dashboard Launcher
echo ================================================
echo.
echo 🚀 Starting ultra-fast quantum dashboard...
echo 📡 URL: http://localhost:5000/fast
echo ⚡ Features: Instant loading, no API delays, demo data
echo.
echo Press Ctrl+C to stop the server
echo ================================================
echo.

cd /d "%~dp0.."
python run_files/run_fast_dashboard.py

pause
