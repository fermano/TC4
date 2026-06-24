from src.report_delivery_retry import retry_delay_seconds


def test_uses_upstream_retry_after_for_502():
    assert retry_delay_seconds(502, {"Retry-After": "30"}) == 30
