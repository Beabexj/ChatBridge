import json
import os

CONFIG_FILE = "config.json"
DEFAULT_CONFIG = {
    "hotkey": "F8",
    "source_lang": "th",
    "target_lang": "en"
}

def load_config():
    """Load configuration from file, or create a default one if it doesn't exist."""
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        return DEFAULT_CONFIG
    
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Error reading config.json. Using default configuration.")
        return DEFAULT_CONFIG
