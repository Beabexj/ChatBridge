import logging
import sys
import os
from chatbridge.resources import get_app_dir

# Use portable directory
app_dir = get_app_dir()
logs_dir = app_dir / "logs"
logs_dir.mkdir(exist_ok=True)

logger = logging.getLogger("ChatBridge")
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

log_file_path = logs_dir / "app.log"
file_handler = logging.FileHandler(str(log_file_path), encoding='utf-8')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
