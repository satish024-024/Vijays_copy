# Simple PowerShell script to delete backed up files

Write-Host "Deleting backed up files..." -ForegroundColor Red

# List of files to delete
$filesToDelete = @(
    "check_real_data.py",
    "comprehensive_api_test.py",
    "quick_api_check.py",
    "test_all_apis_real_data.py",
    "test_api_endpoints.py",
    "test_auth_flow.py",
    "test_auth_integration.py",
    "test_dashboard_connection.py",
    "test_dashboard_fixes.py",
    "test_database_integration.py",
    "test_database.py",
    "test_fixed_apis.py",
    "test_offline_functionality.py",
    "test_production_dashboard.py",
    "test_quantum_advantage.py",
    "test_real_job.py",
    "test_simple_dashboard.py",
    "test_watsonx_key.py",
    "test_api.bat",
    "test_api.ps1",
    "test_dashboard_fixes.html",
    "test_js_fixes.html",
    "test_real_job.html",
    "minimal_test.py",
    "quick_test.py",
    "quick_api_test.py",
    "temp_file.py",
    "cleanup_test_users.py",
    "debug_api_key.py",
    "hackathon_app.py",
    "hackathon_dashboard_app.py",
    "professional_app.py",
    "quantum_app_clean.py",
    "run_hackathon_fixed.py",
    "run_hackathon_simple.py",
    "run_professional_simple.py",
    "run_working_dashboard.py",
    "apply_timeout_fixes.py",
    "timeout_fix.js",
    "TIMEOUT_FIXES_SUMMARY.md",
    "API_TESTING_README.md",
    "AUTHENTICATION_README.md",
    "BLOCH_SPHERE_INTEGRATION.md",
    "DASHBOARD_FIXES_COMPLETE.md",
    "DASHBOARD_FIXES_SUMMARY.md",
    "DATABASE_INTEGRATION.md",
    "EXTERNAL_INTEGRATIONS.md",
    "IMPLEMENTATION_SUMMARY.md",
    "OFFLINE_README.md",
    "PRODUCTION_DASHBOARD_SUMMARY.md",
    "QUANTUM_ADVANTAGE_README.md",
    "QUICK_START_WORKING_DASHBOARD.md",
    "TIMEOUT_FIXES_SUMMARY.md"
)

$deletedCount = 0
$notFoundCount = 0

foreach ($file in $filesToDelete) {
    if (Test-Path $file) {
        Remove-Item $file -Force
        Write-Host "Deleted: $file" -ForegroundColor Red
        $deletedCount++
    } else {
        Write-Host "File not found: $file" -ForegroundColor Yellow
        $notFoundCount++
    }
}

Write-Host ""
Write-Host "DELETION SUMMARY:" -ForegroundColor Cyan
Write-Host "   Files deleted: $deletedCount" -ForegroundColor Red
Write-Host "   Files not found: $notFoundCount" -ForegroundColor Yellow
Write-Host "   Backup location: backup_files\" -ForegroundColor Blue
Write-Host ""
Write-Host "Cleanup completed successfully!" -ForegroundColor Green
Write-Host "   All backed up files have been deleted." -ForegroundColor White
Write-Host "   Main application files are preserved." -ForegroundColor White
Write-Host "   To restore any file: copy backup_files\filename back to main directory" -ForegroundColor White
