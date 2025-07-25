def create_success_block(title, message, emoji="✅"):
    return [{"type": "section", "text": {"type": "mrkdwn", "text": f"{emoji} *{title}*\n{message}"}}]

def create_error_block(title, message, emoji="❌"):
    return [{"type": "section", "text": {"type": "mrkdwn", "text": f"{emoji} *{title}*\n{message}"}}]

def create_info_block(title, message, emoji="ℹ️"):
    return [{"type": "section", "text": {"type": "mrkdwn", "text": f"{emoji} *{title}*\n{message}"}}]