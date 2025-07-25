from datetime import timedelta

def parse_duration(duration_str="1h"):
    if 'h' in duration_str:
        hours = int(duration_str.split('h')[0])
        return timedelta(hours=hours)
    if 'm' in duration_str:
        minutes = int(duration_str.split('m')[0])
        return timedelta(minutes=minutes)
    return timedelta(hours=1)