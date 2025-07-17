import json
import os
import re
from datetime import datetime
from flask import current_app

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output'))
ALLOWED_EXTENSIONS = {'.pdf', '.html', '.md'}
FILENAME_RE = re.compile(r'^briefing_(\d{4}-\d{2}-\d{2})(?:_[\w-]+)?\.(pdf|html|md)$')

def list_briefings():
    """
    Scan OUTPUT_DIR for briefing files, group by date, and return metadata.
    Returns:
        dict: {date: { 'files': {format: filename, ...}, 'datetime': datetime_obj }}
    """
    briefings = {}
    for fname in os.listdir(OUTPUT_DIR):
        match = FILENAME_RE.match(fname)
        if match:
            date_str, ext = match.groups()
            ext = '.' + ext
            if ext not in ALLOWED_EXTENSIONS:
                continue
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            if date_str not in briefings:
                briefings[date_str] = {
                    'files': {},
                    'datetime': date_obj,
                }
            briefings[date_str]['files'][ext[1:]] = fname  # e.g., 'pdf': filename
    # Sort by date descending
    return dict(sorted(briefings.items(), key=lambda x: x[1]['datetime'], reverse=True))

def get_config_path():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')

def get_default_config_path():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config_default.json')

def load_config():
    path = get_config_path()
    with open(path, 'r') as f:
        return json.load(f)

def save_config(config):
    path = get_config_path()
    with open(path, 'w') as f:
        json.dump(config, f, indent=2)

def reset_config():
    default_path = get_default_config_path()
    config_path = get_config_path()
    with open(default_path, 'r') as src, open(config_path, 'w') as dst:
        dst.write(src.read()) 