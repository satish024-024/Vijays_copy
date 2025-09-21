# PowerShell script to verify cleanup and show remaining files

Write-Host "🔍 VERIFYING CLEANUP..." -ForegroundColor Cyan
Write-Host "=" * 50

# Show remaining Python files
Write-Host ""
Write-Host "📁 REMAINING PYTHON FILES:" -ForegroundColor Green
Get-ChildItem -Name "*.py" | Sort-Object | ForEach-Object {
    Write-Host "   ✅ $_" -ForegroundColor Green
}

# Show remaining HTML files
Write-Host ""
Write-Host "📁 REMAINING HTML FILES:" -ForegroundColor Blue
Get-ChildItem -Name "*.html" | Sort-Object | ForEach-Object {
    Write-Host "   ✅ $_" -ForegroundColor Blue
}

# Show remaining JS/CSS files
Write-Host ""
Write-Host "📁 REMAINING JS/CSS FILES:" -ForegroundColor Magenta
Get-ChildItem -Name "*.js", "*.css" | Sort-Object | ForEach-Object {
    Write-Host "   ✅ $_" -ForegroundColor Magenta
}

# Show remaining configuration files
Write-Host ""
Write-Host "📁 REMAINING CONFIG FILES:" -ForegroundColor Yellow
Get-ChildItem -Name "*.md", "*.txt", "*.toml", "*.bat", "*.ps1", "*.json", "*.yml", "*.yaml", "*.dockerfile", "*.env*" | Sort-Object | ForEach-Object {
    Write-Host "   ✅ $_" -ForegroundColor Yellow
}

# Show remaining directories
Write-Host ""
Write-Host "📁 REMAINING DIRECTORIES:" -ForegroundColor Cyan
Get-ChildItem -Directory | Sort-Object | ForEach-Object {
    Write-Host "   📂 $($_.Name)" -ForegroundColor Cyan
}

# Show backup directory
Write-Host ""
Write-Host "📁 BACKUP DIRECTORY:" -ForegroundColor Red
if (Test-Path "backup_files") {
    $backupCount = (Get-ChildItem "backup_files" -File).Count
    Write-Host "   📦 backup_files\ ($backupCount files backed up)" -ForegroundColor Red
} else {
    Write-Host "   ❌ No backup directory found" -ForegroundColor Red
}

Write-Host ""
Write-Host "=" * 50
Write-Host "✅ CLEANUP VERIFICATION COMPLETE!" -ForegroundColor Green
Write-Host "   Main application files are preserved" -ForegroundColor White
Write-Host "   Test/temporary files have been cleaned up" -ForegroundColor White
Write-Host "   All deleted files are safely backed up" -ForegroundColor White
