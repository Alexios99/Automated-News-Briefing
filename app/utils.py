import json
import os
import re
from datetime import datetime
from flask import current_app

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output'))
ALLOWED_EXTENSIONS = {'.pdf', '.html', '.md'}
FILENAME_RE = re.compile(r'^briefing_(\d{4}-\d{2}-\d{2})(?:_([\w-]+))?\.(pdf|html|md)$')

def list_briefings():
    """
    Scan OUTPUT_DIR for briefing files, group by date and custom name, and return metadata.
    Returns:
        dict: {group_key: { 'name': str, 'files': {format: filename, ...}, 'datetime': datetime_obj }}
    """
    briefings = {}
    if not os.path.exists(OUTPUT_DIR):
        return {}
    for entry in os.scandir(OUTPUT_DIR):
        if entry.is_file():
            match = FILENAME_RE.match(entry.name)
            if match:
                date_str, custom_name, ext = match.groups()
                ext = ext.lower()
                if f".{ext}" not in ALLOWED_EXTENSIONS:
                    continue
                
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                group_key = f"{date_str}_{custom_name or 'daily'}"
                
                if group_key not in briefings:
                    briefings[group_key] = {
                        'name': f"Briefing for {date_str}" + (f" ({custom_name.replace('_', ' ').title()})" if custom_name else ""),
                        'files': {},
                        'datetime': date_obj,
                        'date': date_str,
                        'custom_name': custom_name
                    }
                briefings[group_key]['files'][ext] = entry.name
                
    # Sort by date descending, then by name
    return dict(sorted(briefings.items(), key=lambda x: (x[1]['datetime'], x[1]['name']), reverse=True))

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