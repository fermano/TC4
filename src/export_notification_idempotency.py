_delivered_jobs = set()


def should_send_completion(job_id):
    if job_id in _delivered_jobs:
        return False
    _delivered_jobs.add(job_id)
    return True


def clear_delivered_jobs():
    _delivered_jobs.clear()
