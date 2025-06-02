import os
import logging

LOG_DIR = 'logs'
os.makedirs(LOG_DIR, exist_ok=True)

def setup_post_logger():
    logger = logging.getLogger('post_logger')
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        file_handler = logging.FileHandler(os.path.join(LOG_DIR, 'post_requests.log'))
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger

def setup_error_logger():
    logger = logging.getLogger('error_logger')
    logger.setLevel(logging.ERROR)
    if not logger.handlers:
        file_handler = logging.FileHandler(os.path.join(LOG_DIR, 'errors.log'))
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)