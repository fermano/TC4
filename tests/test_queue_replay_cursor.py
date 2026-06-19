from src.queue_replay_cursor import queue_retry_cursor


def test_queue_cursor_advances_acknowledged_event():
    assert queue_retry_cursor({"last_acknowledged": 19}) == 20
