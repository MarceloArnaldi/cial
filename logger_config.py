import os
import logging
from logging.handlers import RotatingFileHandler

LOG_DIR = 'logs'
os.makedirs(LOG_DIR, exist_ok=True)

def setup_rotating_logger(name, filename, level=logging.INFO, max_bytes=1024 * 1024, backup_count=5):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        log_path = os.path.join(LOG_DIR, filename)
        handler = RotatingFileHandler(
            log_path,
            maxBytes=max_bytes,         
            backupCount=backup_count    
        )
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

def setup_post_logger():
    return setup_rotating_logger('post_logger', 'post_requests.log', level=logging.INFO)

def setup_error_logger():
    return setup_rotating_logger('error_logger', 'errors.log', level=logging.ERROR)
