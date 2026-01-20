"""Time parsing utilities for duration strings."""
import re
import logging
from datetime import timedelta
from typing import Optional

logger = logging.getLogger(__name__)


def parse_duration(duration_str: str = "1h") -> timedelta:
    """
    Parse a duration string into a timedelta object.
    
    Supports formats like:
    - "30m" for 30 minutes
    - "1h" for 1 hour
    - "2h" for 2 hours
    - "12h" for 12 hours
    
    Args:
        duration_str: Duration string in format like "1h" or "30m"
        
    Returns:
        timedelta: Parsed duration object
        
    Raises:
        ValueError: If the duration string format is invalid
    """
    if not duration_str or not isinstance(duration_str, str):
        logger.warning(f"Invalid duration string: {duration_str}, defaulting to 1h")
        return timedelta(hours=1)
    
    duration_str = duration_str.strip().lower()
    
    # Match hours: "1h", "2h", "12h", etc.
    hour_match = re.match(r'^(\d+)h$', duration_str)
    if hour_match:
        hours = int(hour_match.group(1))
        if hours < 1 or hours > 12:
            logger.warning(f"Hours out of range (1-12): {hours}, defaulting to 1h")
            return timedelta(hours=1)
        return timedelta(hours=hours)
    
    # Match minutes: "30m", "45m", etc.
    minute_match = re.match(r'^(\d+)m$', duration_str)
    if minute_match:
        minutes = int(minute_match.group(1))
        if minutes < 30 or minutes > 720:  # 30 minutes to 12 hours
            logger.warning(f"Minutes out of range (30-720): {minutes}, defaulting to 1h")
            return timedelta(hours=1)
        return timedelta(minutes=minutes)
    
    # Default to 1 hour if format is invalid
    logger.warning(f"Invalid duration format: {duration_str}, defaulting to 1h")
    return timedelta(hours=1)