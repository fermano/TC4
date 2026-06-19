def retry_delay_seconds(status_code, headers):
    if status_code == 502:
        return 12
    return 0
