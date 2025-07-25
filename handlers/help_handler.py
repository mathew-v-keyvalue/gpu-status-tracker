def handle_help(args, user_id, user_name): # Add args to match signature
    return [
        {"type": "header", "text": {"type": "plain_text", "text": "🤖 GPU Tracker Bot - Help"}},
        {"type": "divider"},
        {"type": "section", "text": {"type": "mrkdwn", "text": "📊 *Status Commands*\n• `/gpu status` or `/gpu` - Check allocation status\n• `/gpu realtime` - View real-time GPU performance"}},
        {"type": "section", "text": {"type": "mrkdwn", "text": "🎯 *Management Commands*\n• `/gpu claim <id> <purpose> [duration]` - Reserve a GPU\n• `/gpu release <id>` - Release your claimed GPU"}},
        {"type": "divider"},
        {"type": "section", "text": {"type": "mrkdwn", "text": "💡 *Examples*\n```\n/gpu claim 0 training model 3h\n/gpu release 1\n```"}}
    ]