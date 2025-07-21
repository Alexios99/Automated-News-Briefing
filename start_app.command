#!/bin/bash

clear
echo "============================================="
echo "  Automated News Briefing - Quick Launcher  "
echo "============================================="

# Check for python3
if ! command -v python3 &> /dev/null
then
    echo "Python 3 is not installed. Please install it from https://www.python.org/downloads/"
    read -n 1 -s -r -p "Press any key to close this window..."
    exit 1
fi

# Check if venv exists
if [ -d "venv" ]; then
    echo "Detected existing setup. Launching the app..."
    source venv/bin/activate
    echo "Starting the app. Please wait a few seconds..."
    sleep 3
    open http://127.0.0.1:5000
    python3 app.py
    echo
    echo "If the app did not start or you see errors above, please check your setup."
    read -n 1 -s -r -p "Press any key to close this window..."
    exit 0
fi

# Run setup.py for first-time setup
python3 setup.py

echo "Opening the app in your browser..."
sleep 3
open http://127.0.0.1:5000

echo
echo "If the app did not start, please check for errors above."
read -n 1 -s -r -p "Press any key to close this window..." 