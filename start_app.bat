@echo off

REM Friendly welcome
cls
echo =============================================
echo   Automated News Briefing - Quick Launcher
echo =============================================

REM Check for Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python 3.8 or higher from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Running setup and launching the app...
python setup.py

echo.
echo If the app did not start, please check for errors above.
pause 