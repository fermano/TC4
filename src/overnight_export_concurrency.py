def overnight_export_concurrency(pending_exports):
    if pending_exports >= 1000:
        return 10
    return 4
