"""Handler for GPU status display commands."""
import logging
from datetime import datetime, timezone
from typing import List, Dict, Any
from config import INDIA_TZ, TOTAL_GPUS
from utils.status_manager import get_status, save_status

logger = logging.getLogger(__name__)


def _check_and_expire_claims(status: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check for expired claims and automatically release them.
    
    Args:
        status: Current status dictionary
        
    Returns:
        Updated status dictionary with expired claims released
    """
    now = datetime.now(timezone.utc)
    updated = False
    
    for gpu_id, info in status.items():
        if info.get('status') == 'in_use' and 'release_time' in info:
            try:
                release_time = datetime.fromisoformat(info['release_time']).replace(tzinfo=timezone.utc)
                if now >= release_time:
                    logger.info(f"Auto-releasing expired GPU {gpu_id} (claimed by {info.get('user_name', 'Unknown')})")
                    status[gpu_id] = {"status": "available"}
                    updated = True
            except (ValueError, KeyError) as e:
                logger.warning(f"Error parsing release_time for GPU {gpu_id}: {e}")
    
    if updated:
        try:
            save_status(status)
        except Exception as e:
            logger.error(f"Failed to save auto-released status: {e}")
    
    return status


def handle_status(args: List[str], user_id: str, user_name: str) -> List[Dict[str, Any]]:
    """
    Handle GPU status display command.
    
    Args:
        args: Command arguments (unused)
        user_id: Slack user ID
        user_name: Slack user name
        
    Returns:
        List of Slack block elements for the response
    """
    try:
        status = get_status()
        status = _check_and_expire_claims(status)
    except Exception as e:
        logger.error(f"Failed to get status: {e}")
        return [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "❌ *Error*\nFailed to retrieve GPU status. Please try again later."
                }
            }
        ]
    
    current_time = datetime.now(INDIA_TZ).strftime('%I:%M %p IST, %B %d')
    blocks = [
        {"type": "header", "text": {"type": "plain_text", "text": "🎯 GPU Allocation Dashboard"}},
        {
            "type": "context",
            "elements": [{"type": "mrkdwn", "text": f"📅 Updated: {current_time} | Total GPUs: {TOTAL_GPUS}"}]
        },
        {"type": "divider"}
    ]
    
    for gpu_id in sorted(status.keys(), key=int):
        info = status[gpu_id]
        if info.get('status') == 'available':
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"✅ *GPU {gpu_id}*\nStatus: Available for use"
                }
            })
        else:
            try:
                release_time_str = "Unknown"
                remaining_str = ""
                
                if 'release_time' in info:
                    utc_time = datetime.fromisoformat(info['release_time']).replace(tzinfo=timezone.utc)
                    ist_time = utc_time.astimezone(INDIA_TZ)
                    release_time_str = ist_time.strftime('%I:%M %p IST')
                    
                    # Calculate remaining time
                    now = datetime.now(timezone.utc)
                    remaining = utc_time - now
                    if remaining.total_seconds() > 0:
                        hours = int(remaining.total_seconds() // 3600)
                        minutes = int((remaining.total_seconds() % 3600) // 60)
                        if hours > 0:
                            remaining_str = f"⏳ {hours}h {minutes}m remaining"
                        else:
                            remaining_str = f"⏳ {minutes}m remaining"
                    else:
                        remaining_str = "⏳ Expired"
                
                user_name_display = info.get('user_name', 'Unknown')
                purpose = info.get('purpose', 'No purpose specified')
                
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"🔴 *GPU {gpu_id} - In Use*\n👤 User: {user_name_display}\n📝 Purpose: `{purpose}`\n⏰ Until: ~{release_time_str}\n{remaining_str}"
                    }
                })
            except (ValueError, KeyError) as e:
                logger.warning(f"Error formatting GPU {gpu_id} status: {e}")
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"⚠️ *GPU {gpu_id}*\nStatus: In use (details unavailable)"
                    }
                })
        
        blocks.append({"type": "divider"})
    
    blocks.append({
        "type": "context",
        "elements": [{"type": "mrkdwn", "text": "💡 Use `/gpu claim <id> <purpose> [duration]` to reserve a GPU"}]
    })
    
    return blocks