from datetime import datetime, timezone
from config import INDIA_TZ
from utils.status_manager import get_status, save_status
from utils.slack_blocks import create_error_block
from utils.time_parser import parse_duration

def handle_claim(args, user_id, user_name):
    if len(args) < 2:
        return create_error_block(
            "Invalid Command Format",
            "Please use: `/gpu claim <number> <purpose> [duration]`\n\n*Example:* `/gpu claim 0 training model 2h`"
        )

    gpu_id = args[0]
    status = get_status()

    if gpu_id not in status:
        available_gpus = ", ".join(f"`{k}`" for k in status.keys())
        return create_error_block("GPU Not Found", f"GPU `{gpu_id}` does not exist.\n*Available GPUs:* {available_gpus}")
    
    if status[gpu_id]['status'] != 'available':
        return create_error_block("GPU Already in Use", f"GPU `{gpu_id}` is currently being used by *{status[gpu_id]['user_name']}*.")

    duration_str = args[-1] if args[-1].endswith(('h', 'm')) else "1h"
    purpose = " ".join(args[1:-1]) if duration_str != "1h" else " ".join(args[1:])
    if not purpose: purpose = "No purpose specified"

    claim_time = datetime.utcnow()
    release_time = claim_time + parse_duration(duration_str)
    release_time_ist = release_time.replace(tzinfo=timezone.utc).astimezone(INDIA_TZ).strftime('%I:%M %p IST')

    status[gpu_id] = {"status": "in_use", "user_id": user_id, "user_name": user_name, "purpose": purpose, "claim_time": claim_time.isoformat(), "release_time": release_time.isoformat()}
    save_status(status)
    
    return [{"type": "section", "text": {"type": "mrkdwn", "text": f"🎉 *GPU {gpu_id} Successfully Claimed!*\n\n👤 *User:* {user_name}\n📝 *Purpose:* `{purpose}`\n⏰ *Duration:* {duration_str}\n🕒 *Release Time:* ~{release_time_ist}"}},
            {"type": "context", "elements": [{"type": "mrkdwn", "text": f"💡 _Remember to use `/gpu release {gpu_id}` when you're done!_"}]}]