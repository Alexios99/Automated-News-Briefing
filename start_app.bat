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
    REM Activate venv and run app.py directly
    call venv\Scripts\activate
    start "" http://127.0.0.1:5000
    python app.py
    goto :eof
)

REM Run setup.py for first-time setup
python setup.py

REM Open browser after setup (if not already open)
start "" http://127.0.0.1:5000

REM Pause so the window stays open if there's an error
echo.
echo If the app did not start, please check for errors above.
pause 