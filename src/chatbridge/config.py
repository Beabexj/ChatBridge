import json
import os
from pathlib import Path
from chatbridge.logger import logger
from chatbridge.resources import get_app_dir

def get_config_path() -> Path:
    return get_app_dir() / "config.json"

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
    config_file = get_config_path()
    if not config_file.exists():
        return save_config(DEFAULT_CONFIG)
    
    try:
        with open(config_file, "r", encoding="utf-8") as f:
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
    config_file = get_config_path()
    try:
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=4)
        logger.info("Configuration saved successfully.")
    except Exception as e:
        logger.error(f"Error saving config.json: {e}")
    return config_data
