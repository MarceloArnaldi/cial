import os
import json
from flask import Response, abort, jsonify
from config.logger_config import setup_error_logger

LOG_DIR = 'logs'
LOG_FILES = {
    'post': os.path.join(LOG_DIR, 'post_requests.log'),
    'error': os.path.join(LOG_DIR, 'errors.log'),
}

error_logger = setup_error_logger()

def get_logs(log_type):
    print('log_type')
    print(log_type)
    if log_type not in ['post','error']:
        return {
            "body"   : { "error" : "accepted paths /logs/post or /logs/error" },
            "status" : 422
        }
    file_path = LOG_FILES.get(log_type)
    if not file_path or not os.path.isfile(file_path):
        return {
            "body"   : { "error" : "log file not found." },
            "status" : 404
        }
    try:
        lines = []
        with open(file_path, 'r') as f:
            lines = f.readlines()[-100:]
        return {
            "body"   : { log_type : lines },
            "status" : 200
        }
    except Exception as e:
        error_logger.error(f"error reading log {log_type}: {str(e)}")
        return {
            "body"   : { "error" : f"error reading log {log_type}: {str(e)}" },
            "status" : 500
        }
