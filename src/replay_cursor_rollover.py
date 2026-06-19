def next_replay_cursor(last_acknowledged, attempted_batch_size):
    if last_acknowledged < 0:
        raise ValueError("last acknowledged cursor must be non-negative")
    return last_acknowledged + 1
