def queue_retry_cursor(payload):
    acknowledged = payload.get("last_acknowledged", 0)
    return acknowledged + 1
