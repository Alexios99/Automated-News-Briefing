@echo off

REM Friendly welcome
cls
echo =============================================
echo   Automated News Briefing - Quick Launcher
echo =============================================

REM Try to find python or python3
where python >nul 2>nul
if %errorlevel%==0 (
    set PYTHON_CMD=python
) else (
    where python3 >nul 2>nul
    if %errorlevel%==0 (
        set PYTHON_CMD=python3
    ) else (
        echo Python is not installed or not in your PATH.
        echo Please install Python 3.8+ from https://www.python.org/downloads/
        echo And make sure to check "Add Python to PATH" during installation.
        pause
        exit /b 1
    )
)

echo Running setup and launching the app...
%PYTHON_CMD% setup.py

echo.
echo If the app did not start, please check for errors above.
pause 