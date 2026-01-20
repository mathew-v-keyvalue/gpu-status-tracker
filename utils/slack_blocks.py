"""Slack Block Kit UI component builders."""
from typing import List, Dict, Any


def create_success_block(title: str, message: str, emoji: str = "✅") -> List[Dict[str, Any]]:
    """
    Create a success message block for Slack.
    
    Args:
        title: Title of the success message
        message: Detailed message content
        emoji: Emoji to display (default: ✅)
        
    Returns:
        List of Slack block elements
    """
    return [{"type": "section", "text": {"type": "mrkdwn", "text": f"{emoji} *{title}*\n{message}"}}]


def create_error_block(title: str, message: str, emoji: str = "❌") -> List[Dict[str, Any]]:
    """
    Create an error message block for Slack.
    
    Args:
        title: Title of the error message
        message: Detailed error message
        emoji: Emoji to display (default: ❌)
        
    Returns:
        List of Slack block elements
    """
    return [{"type": "section", "text": {"type": "mrkdwn", "text": f"{emoji} *{title}*\n{message}"}}]


def create_info_block(title: str, message: str, emoji: str = "ℹ️") -> List[Dict[str, Any]]:
    """
    Create an info message block for Slack.
    
    Args:
        title: Title of the info message
        message: Detailed message content
        emoji: Emoji to display (default: ℹ️)
        
    Returns:
        List of Slack block elements
    """
    return [{"type": "section", "text": {"type": "mrkdwn", "text": f"{emoji} *{title}*\n{message}"}}]