"""Handler for help command."""
from typing import List, Dict, Any


def handle_help(args: List[str], user_id: str, user_name: str) -> List[Dict[str, Any]]:
    """
    Handle help command to display usage information.
    
    Args:
        args: Command arguments (unused)
        user_id: Slack user ID
        user_name: Slack user name
        
    Returns:
        List of Slack block elements for the response
    """
    return [
        {"type": "header", "text": {"type": "plain_text", "text": "🤖 GPU Tracker Bot - Help Guide"}},
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "📊 *Status Commands*\n• `/gpu status` or `/gpu` - Check allocation status\n• `/gpu realtime` - View real-time GPU performance"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "🎯 *Management Commands*\n• `/gpu claim <id> <purpose> [duration]` - Reserve a GPU\n• `/gpu release <id>` - Release your claimed GPU"
            }
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "💡 *Examples*\n```\n/gpu claim 0 training model 3h\n/gpu release 1\n/gpu realtime\n/gpu status\n```"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "⏰ *Duration Formats*\n• `30m` - 30 minutes\n• `1h` - 1 hour\n• `2h` - 2 hours\n• `4h` - 4 hours\n• `8h` - 8 hours\n• `12h` - 12 hours"
            }
        },
        {
            "type": "context",
            "elements": [{"type": "mrkdwn", "text": "💡 _Claims automatically expire at the specified release time_"}]
        }
    ]