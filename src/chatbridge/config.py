import json
import os
from chatbridge.logger import logger

CONFIG_FILE = "config.json"
DEFAULT_CONFIG = {
    "hotkey": "F8",
    "source_lang": "auto",
    "target_lang": "en",
    "auto_send": False,
    "enabled": True,
    "start_with_windows": False,
    "log_level": "INFO"
}

def load_config():
    """Load configuration from file, or create a default one if it doesn't exist."""
    if not os.path.exists(CONFIG_FILE):
        return save_config(DEFAULT_CONFIG)
    
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
            # Merge with default config to ensure all keys exist
            merged = DEFAULT_CONFIG.copy()
            merged.update(config)
            return merged
    except json.JSONDecodeError:
        logger.warning("Error reading config.json. Using default configuration.")
        return save_config(DEFAULT_CONFIG)

def save_config(config_data):
    """Save configuration dict to file."""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=4)
        logger.info("Configuration saved successfully.")
    except Exception as e:
        logger.error(f"Error saving config.json: {e}")
    return config_data
