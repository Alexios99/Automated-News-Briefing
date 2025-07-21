import sys
import subprocess
import os
import json
import venv
from pathlib import Path

# --- Configuration ---
VENV_DIR = "venv"
REQUIREMENTS_FILE = "requirements.txt"
CONFIG_FILE = "config.json"
DEFAULT_CONFIG_FILE = "config_default.json"
REQUIRED_KEYS = ["NEWS_API_KEY", "GOOGLE_API_KEY", "MARKETAUX_API_TOKEN"]

def get_executable(name):
    """
    Returns the path to an executable within the virtual environment.
    Handles differences between Windows and Unix-like systems.
    """
    if sys.platform == "win32":
        return Path(VENV_DIR) / "Scripts" / f"{name}.exe"
    else:
        return Path(VENV_DIR) / "bin" / name

def check_python_version():
    """Checks if the Python version is 3.8 or higher."""
    if sys.version_info < (3, 8):
        print("Error: This project requires Python 3.8 or higher.")
        print(f"You are using Python {sys.version_info.major}.{sys.version_info.minor}.")
        sys.exit(1)
    print(f"✓ Python version is compatible ({sys.version_info.major}.{sys.version_info.minor}).")

def create_virtual_environment():
    """Creates a virtual environment if it doesn't already exist."""
    if not os.path.isdir(VENV_DIR):
        print(f"Creating virtual environment in './{VENV_DIR}'...")
        venv.create(VENV_DIR, with_pip=True)
        print("✓ Virtual environment created.")
    else:
        print("✓ Virtual environment already exists.")

def install_dependencies():
    """Installs dependencies from requirements.txt into the venv."""
    print("Installing required packages...")
    pip_executable = get_executable("pip")
    try:
        subprocess.check_call([str(pip_executable), "install", "-r", REQUIREMENTS_FILE])
        print("✓ Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to install dependencies. {e}")
        sys.exit(1)

def install_playwright_browsers():
    """Installs the necessary Playwright browsers."""
    print("Installing Playwright browsers (this may take a moment)...")
    playwright_executable = get_executable("playwright")
    try:
        subprocess.check_call([str(playwright_executable), "install", "--with-deps"])
        print("✓ Playwright browsers installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to install Playwright browsers. {e}")
        sys.exit(1)

def configure_application():
    """
    Ensures config.json exists and contains the necessary API keys.
    Prompts the user if keys are missing.
    """
    if not os.path.exists(CONFIG_FILE):
        print(f"'{CONFIG_FILE}' not found. Copying from default...")
        try:
            with open(DEFAULT_CONFIG_FILE, 'r') as src, open(CONFIG_FILE, 'w') as dest:
                dest.write(src.read())
            print(f"✓ Created '{CONFIG_FILE}'.")
        except FileNotFoundError:
            print(f"Error: '{DEFAULT_CONFIG_FILE}' not found. Cannot create config.")
            sys.exit(1)

    # Now, check for keys
    config_needs_update = False
    with open(CONFIG_FILE, 'r+') as f:
        config_data = json.load(f)
        
        for key in REQUIRED_KEYS:
            if not config_data.get(key): # Checks for None or empty string
                print(f"API Key '{key}' is missing.")
                value = input(f"Please enter your {key}: ")
                config_data[key] = value
                config_needs_update = True
        
        if config_needs_update:
            f.seek(0)
            json.dump(config_data, f, indent=4)
            f.truncate()
            print("✓ Configuration updated with your API keys.")
        else:
            print("✓ API keys are already configured.")

def launch_application():
    """Launches the Flask web application."""
    print("\n-----------------------------------------------------")
    print("Setup complete. Launching the web application...")
    print("Access it at: http://127.0.0.1:5000")
    print("Press CTRL+C in this window to stop the server.")
    print("-----------------------------------------------------")
    
    python_executable = get_executable("python")
    try:
        subprocess.check_call([str(python_executable), "app.py"])
    except KeyboardInterrupt:
        print("\nApplication stopped by user.")
    except Exception as e:
        print(f"\nAn error occurred while running the application: {e}")

if __name__ == "__main__":
    print("--- Automated News Briefing Setup ---")
    check_python_version()
    create_virtual_environment()
    install_dependencies()
    install_playwright_browsers()
    configure_application()
    launch_application() 