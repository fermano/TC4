from src.overnight_export_concurrency import overnight_export_concurrency


def test_large_batch_uses_tested_concurrency_ceiling():
    assert overnight_export_concurrency(1000) == 8


def test_routine_batch_keeps_default_concurrency():
    assert overnight_export_concurrency(100) == 4
