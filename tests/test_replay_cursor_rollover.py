from src.replay_cursor_rollover import next_replay_cursor


def test_advances_from_last_acknowledged_cursor():
    assert next_replay_cursor(19, attempted_batch_size=5) == 20
