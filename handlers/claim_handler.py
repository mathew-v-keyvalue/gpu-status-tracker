"""Handler for GPU claim commands."""
import logging
from datetime import datetime, timezone
from typing import List, Dict, Any
from config import INDIA_TZ
from utils.status_manager import get_status, save_status, validate_gpu_id
from utils.slack_blocks import create_error_block
from utils.time_parser import parse_duration

logger = logging.getLogger(__name__)


def handle_claim(args: List[str], user_id: str, user_name: str) -> List[Dict[str, Any]]:
    """
    Handle GPU claim command.
    
    Args:
        args: Command arguments [gpu_id, purpose, ...duration]
        user_id: Slack user ID
        user_name: Slack user name
        
    Returns:
        List of Slack block elements for the response
    """
    if len(args) < 2:
        return create_error_block(
            "Invalid Command Format",
            "Please use: `/gpu claim <number> <purpose> [duration]`\n\n*Example:* `/gpu claim 0 training model 2h`"
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
            f"GPU `{gpu_id}` does not exist.\n*Available GPUs:* {available_gpus}"
        )
    
    if status[gpu_id]['status'] != 'available':
        current_user = status[gpu_id].get('user_name', 'Unknown')
        return create_error_block(
            "GPU Already in Use",
            f"GPU `{gpu_id}` is currently being used by *{current_user}*."
        )

    # Parse duration - check if last arg is a duration string
    duration_str = "1h"
    if args[-1].lower().endswith(('h', 'm')):
        duration_str = args[-1].lower()
        purpose = " ".join(args[1:-1]) if len(args) > 2 else "No purpose specified"
    else:
        purpose = " ".join(args[1:])
    
    if not purpose or not purpose.strip():
        purpose = "No purpose specified"

    try:
        duration = parse_duration(duration_str)
    except ValueError as e:
        logger.warning(f"Invalid duration format: {duration_str}, using default 1h")
        duration_str = "1h"
        duration = parse_duration(duration_str)

    claim_time = datetime.now(timezone.utc)
    release_time = claim_time + duration
    release_time_ist = release_time.astimezone(INDIA_TZ).strftime('%I:%M %p IST')

    status[gpu_id] = {
        "status": "in_use",
        "user_id": user_id,
        "user_name": user_name,
        "purpose": purpose,
        "claim_time": claim_time.isoformat(),
        "release_time": release_time.isoformat()
    }
    
    try:
        save_status(status)
        logger.info(f"GPU {gpu_id} claimed by {user_name} ({user_id}) for {duration_str}")
    except Exception as e:
        logger.error(f"Failed to save status: {e}")
        return create_error_block(
            "System Error",
            "Failed to save GPU claim. Please try again later."
        )
    
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"🎉 *GPU {gpu_id} Successfully Claimed!*\n\n👤 *User:* {user_name}\n📝 *Purpose:* `{purpose}`\n⏰ *Duration:* {duration_str}\n🕒 *Release Time:* ~{release_time_ist}"
            }
        },
        {
            "type": "context",
            "elements": [{"type": "mrkdwn", "text": f"💡 _Remember to use `/gpu release {gpu_id}` when you're done!_"}]}
    ]