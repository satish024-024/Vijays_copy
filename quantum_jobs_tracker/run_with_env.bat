@echo off
echo 🚀 Starting Quantum Jobs Tracker with Clean Qiskit Environment...
echo.

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."

REM Activate the virtual environment
echo 🔧 Activating virtual environment...
call "%PROJECT_ROOT%\quantum_env\Scripts\activate.bat"

REM Run the Flask application
echo 🌐 Starting Flask server...
python "%SCRIPT_DIR%real_quantum_app.py"

REM Keep the window open if there's an error
pause
