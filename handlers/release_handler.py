"""Handler for GPU release commands."""
import logging
from typing import List, Dict, Any
from utils.status_manager import get_status, save_status, validate_gpu_id
from utils.slack_blocks import create_error_block, create_info_block

logger = logging.getLogger(__name__)


def handle_release(args: List[str], user_id: str, user_name: str) -> List[Dict[str, Any]]:
    """
    Handle GPU release command.
    
    Args:
        args: Command arguments [gpu_id]
        user_id: Slack user ID
        user_name: Slack user name
        
    Returns:
        List of Slack block elements for the response
    """
    if len(args) < 1:
        return create_error_block(
            "Invalid Command Format",
            "Please use: `/gpu release <number>`\n\n*Example:* `/gpu release 0`"
        )

    gpu_id = args[0].strip()
    
    try:
        status = get_status()
    except Exception as e:
        logger.error(f"Failed to get status: {e}")
        return create_error_block(
            "System Error",
            "Failed to retrieve GPU status. Please try again later."
        )

    if not validate_gpu_id(gpu_id, status):
        available_gpus = ", ".join(f"`{k}`" for k in sorted(status.keys(), key=int))
        return create_error_block(
            "GPU Not Found",
            f"GPU `{gpu_id}` does not exist in the system.\n*Available GPUs:* {available_gpus}"
        )
    
    if status[gpu_id]['status'] == 'available':
        return create_info_block(
            "GPU Already Available",
            f"GPU `{gpu_id}` is already available. No action needed!"
        )
    
    current_user_id = status[gpu_id].get('user_id')
    current_user_name = status[gpu_id].get('user_name', 'Unknown')
    
    if current_user_id != user_id:
        return create_error_block(
            "Permission Denied",
            f"You cannot release GPU `{gpu_id}`. It was claimed by *{current_user_name}*."
        )

    status[gpu_id] = {"status": "available"}
    
    try:
        save_status(status)
        logger.info(f"GPU {gpu_id} released by {user_name} ({user_id})")
    except Exception as e:
        logger.error(f"Failed to save status: {e}")
        return create_error_block(
            "System Error",
            "Failed to save GPU release. Please try again later."
        )
    
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"✅ *GPU {gpu_id} Successfully Released by {user_name}!*\nThank you for freeing it up! 🙏"
            }
        }
    ]
