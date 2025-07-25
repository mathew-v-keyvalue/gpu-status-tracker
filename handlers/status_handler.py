from datetime import datetime, timezone
from config import INDIA_TZ
from utils.status_manager import get_status

def handle_status(args, user_id, user_name): # Add args to match signature
    status = get_status()
    current_time = datetime.now(INDIA_TZ).strftime('%I:%M %p IST, %B %d')
    blocks = [{"type": "header", "text": {"type": "plain_text", "text": "🎯 GPU Allocation Status"}},
              {"type": "context", "elements": [{"type": "mrkdwn", "text": f"📅 Updated: {current_time}"}]},
              {"type": "divider"}]
    
    for gpu_id, info in sorted(status.items()):
        if info['status'] == 'available':
            blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": f"✅ *GPU {gpu_id}:* `Available for use`"}})
        else:
            utc_time = datetime.fromisoformat(info['release_time']).replace(tzinfo=timezone.utc)
            ist_time = utc_time.astimezone(INDIA_TZ)
            release_time_str = ist_time.strftime('%I:%M %p IST')
            blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": f"🔴 *GPU {gpu_id}:* Claimed by *{info['user_name']}* for `{info['purpose']}`\n_Until ~{release_time_str}_"}})
        blocks.append({"type": "divider"})
        
    return blocks