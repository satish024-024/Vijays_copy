@echo off
echo ===============================================
echo    SATISH KUMAR BACKUP - RESTORE SCRIPT
echo ===============================================
echo.
echo This script will restore your quantum computing project
echo to its original state from the Satish Kumar backup.
echo.
echo WARNING: This will overwrite ALL current files!
echo.
set /p confirm="Are you sure you want to restore? (y/N): "
if /i not "%confirm%"=="y" (
    echo Restore cancelled.
    pause
    exit /b 0
)

echo.
echo Starting restore process...
echo.

REM Get the current directory (backup directory)
set "BACKUP_DIR=%~dp0"
set "TARGET_DIR=%BACKUP_DIR%.."

echo Backup Directory: %BACKUP_DIR%
echo Target Directory: %TARGET_DIR%
echo.

REM Create a temporary directory for current files (just in case)
echo Creating safety backup of current state...
mkdir "%TARGET_DIR%\temp_current_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%" 2>nul

REM Copy all files from backup to target directory
echo Restoring files from Satish Kumar backup...
robocopy "%BACKUP_DIR%" "%TARGET_DIR%" /E /XD "Satish_Kumar_Backup_*" "temp_current_backup_*" /XF "RESTORE_TO_ORIGINAL.bat" "README_BACKUP.txt"

if %ERRORLEVEL% LEQ 1 (
    echo.
    echo ===============================================
    echo    RESTORE COMPLETED SUCCESSFULLY!
    echo ===============================================
    echo.
    echo Your quantum computing project has been restored
    echo to its original state from the Satish Kumar backup.
    echo.
    echo The backup was created on: 2025-09-05 at 21:32:48
    echo.
) else (
    echo.
    echo ===============================================
    echo    RESTORE COMPLETED WITH WARNINGS
    echo ===============================================
    echo.
    echo Some files may not have been restored properly.
    echo Please check the output above for details.
    echo.
)

echo Press any key to exit...
pause >nul
