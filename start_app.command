#!/bin/bash

clear
echo "============================================="
echo "  Automated News Briefing - Quick Launcher  "
echo "============================================="

# Check for python3
if ! command -v python3 &> /dev/null
then
    echo "Python 3 is not installed. Please install it from https://www.python.org/downloads/"
    exit 1
fi

# Check if venv exists
if [ -d "venv" ]; then
    echo "Detected existing setup. Launching the app..."
    source venv/bin/activate
    open http://127.0.0.1:5000
    python3 app.py
    exit 0
fi

# Run setup.py for first-time setup
python3 setup.py

# Open browser after setup (if not already open)
open http://127.0.0.1:5000

echo "If the app did not start, please check for errors above."
read -n 1 -s -r -p "Press any key to close this window..." 