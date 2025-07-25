from datetime import datetime
from utils.status_manager import get_status, save_status
from utils.slack_blocks import create_error_block, create_info_block

def handle_release(args, user_id):
    if len(args) < 1:
        return create_error_block("Invalid Command Format", "Please use: `/gpu release <number>`\n\n*Example:* `/gpu release 0`")

    gpu_id = args[0]
    status = get_status()

    if gpu_id not in status:
        return create_error_block("GPU Not Found", f"GPU `{gpu_id}` does not exist in the system.")
    
    if status[gpu_id]['status'] == 'available':
        return create_info_block("GPU Already Available", f"GPU `{gpu_id}` is already available. No action needed!")
    
    if status[gpu_id]['user_id'] != user_id:
        return create_error_block("Permission Denied", f"You cannot release GPU `{gpu_id}`. It was claimed by *{status[gpu_id]['user_name']}*.")

    status[gpu_id] = {"status": "available"}
    save_status(status)
    
    return [{"type": "section", "text": {"type": "mrkdwn", "text": f"✅ *GPU {gpu_id} Successfully Released!*\nThank you for freeing it up! 🙏"}}]