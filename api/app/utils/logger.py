import logging
import sys
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name="bangla_med_rag"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Prevent multiple handlers if setup_logger is called multiple times
    if logger.handlers:
        return logger

    # Create logs directory if it doesn't exist
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)

    # File Handler (Rotating)
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, "api.log"),
        maxBytes=1024 * 1024 * 5,  # 5MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    return logger

logger = setup_logger()
