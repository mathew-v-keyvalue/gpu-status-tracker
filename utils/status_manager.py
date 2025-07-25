import os
import json
from config import TOTAL_GPUS, STATUS_FILE

def initialize_status():
    if not os.path.exists(STATUS_FILE):
        status = {str(i): {"status": "available"} for i in range(TOTAL_GPUS)}
        with open(STATUS_FILE, 'w') as f:
            json.dump(status, f)
    return True

def get_status():
    with open(STATUS_FILE, 'r') as f:
        return json.load(f)

def save_status(status):
    with open(STATUS_FILE, 'w') as f:
        json.dump(status, f, indent=2)