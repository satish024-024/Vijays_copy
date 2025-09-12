@echo off
echo 🚀 Starting Quantum Advantage Research Platform...
echo.

REM Activate virtual environment
call .\quantum_env\Scripts\activate.bat

REM Navigate to quantum_jobs_tracker
cd quantum_jobs_tracker

REM Start the Flask application
echo 🔬 Starting Flask application...
python real_quantum_app.py

REM Keep window open if there's an error
pause
