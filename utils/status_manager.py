"""Status management utilities for GPU tracking."""
import os
import json
import fcntl
import logging
from typing import Dict, Any
from config import TOTAL_GPUS, STATUS_FILE

logger = logging.getLogger(__name__)


def initialize_status() -> bool:
    """
    Initialize the GPU status file if it doesn't exist.
    
    Returns:
        bool: True if initialization was successful
    """
    try:
        if not os.path.exists(STATUS_FILE):
            status = {str(i): {"status": "available"} for i in range(TOTAL_GPUS)}
            with open(STATUS_FILE, 'w') as f:
                json.dump(status, f, indent=2)
            logger.info(f"Initialized status file with {TOTAL_GPUS} GPUs")
        return True
    except (IOError, OSError) as e:
        logger.error(f"Failed to initialize status file: {e}")
        raise


def get_status() -> Dict[str, Any]:
    """
    Read the current GPU status from the file.
    
    Returns:
        Dict[str, Any]: Dictionary containing GPU status information
        
    Raises:
        IOError: If the file cannot be read
        json.JSONDecodeError: If the file contains invalid JSON
    """
    try:
        with open(STATUS_FILE, 'r') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_SH)  # Shared lock for reading
            try:
                return json.load(f)
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    except FileNotFoundError:
        logger.warning("Status file not found, initializing...")
        initialize_status()
        return get_status()
    except (IOError, json.JSONDecodeError) as e:
        logger.error(f"Failed to read status file: {e}")
        raise


def save_status(status: Dict[str, Any]) -> None:
    """
    Save the GPU status to the file with file locking.
    
    Args:
        status: Dictionary containing GPU status information
        
    Raises:
        IOError: If the file cannot be written
    """
    try:
        with open(STATUS_FILE, 'w') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)  # Exclusive lock for writing
            try:
                json.dump(status, f, indent=2)
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        logger.debug("Status file updated successfully")
    except (IOError, OSError) as e:
        logger.error(f"Failed to save status file: {e}")
        raise


def validate_gpu_id(gpu_id: str, status: Dict[str, Any]) -> bool:
    """
    Validate that a GPU ID exists in the status.
    
    Args:
        gpu_id: GPU ID to validate
        status: Current status dictionary
        
    Returns:
        bool: True if GPU ID is valid
    """
    if not gpu_id or not isinstance(gpu_id, str):
        return False
    # Check if it's a valid numeric string that exists in status
    try:
        int(gpu_id)
        return gpu_id in status
    except ValueError:
        return False