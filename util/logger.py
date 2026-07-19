import logging
import os

LOG_DIR = "logs"
LOG_FILE = "vulnops.log"

os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("VulnOps")
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

file_handler = logging.FileHandler(os.path.join(LOG_DIR, LOG_FILE))
file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)