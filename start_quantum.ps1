# Quantum Advantage Research Platform Launcher
Write-Host "Starting Quantum Advantage Research Platform..." -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (!(Test-Path ".\quantum_env\Scripts\Activate.ps1")) {
    Write-Host "Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run: python -m venv quantum_env" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Green
& .\quantum_env\Scripts\Activate.ps1

# Navigate to quantum_jobs_tracker
Write-Host "Changing to quantum_jobs_tracker directory..." -ForegroundColor Green
Set-Location quantum_jobs_tracker

# Start the Flask application
Write-Host "Starting Flask application..." -ForegroundColor Green
Write-Host "Access at: http://localhost:10000" -ForegroundColor Cyan
Write-Host "Research Platform: http://localhost:10000/quantum-research" -ForegroundColor Cyan
Write-Host ""

python real_quantum_app.py
