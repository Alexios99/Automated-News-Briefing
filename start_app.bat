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

REM Check if venv exists
if exist venv (
    echo Detected existing setup. Launching the app...
    call venv\Scripts\activate
    echo Starting the app. Please wait a few seconds...
    timeout /t 3 >nul
    start "" http://127.0.0.1:5000
    python app.py
    echo.
    echo If the app did not start or you see errors above, please check your setup.
    pause
    goto :eof
)

REM Run setup.py for first-time setup
python setup.py

REM Wait a moment, then open browser after setup (if not already open)
echo Opening the app in your browser...
timeout /t 3 >nul
start "" http://127.0.0.1:5000

echo.
echo If the app did not start, please check for errors above.
pause 