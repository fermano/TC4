from datetime import datetime, timezone

import pytest

from src.ops_service import (
    OperationSignal,
    build_release_marker,
    group_signals_by_owner,
    highest_severity,
    normalize_owner,
    parse_release_marker,
    summarize_signals_for_handoff,
)


def test_normalize_owner_defaults_blank_values():
    assert normalize_owner("   ") == "unassigned"


def test_group_signals_by_owner_uses_fallback_owner_for_blank_handoffs():
    signal = OperationSignal("handoff", "high", "   ", datetime.now(timezone.utc))

    grouped = group_signals_by_owner([signal], fallback_owner="Engineering Ops")

    assert grouped == {"engineering-ops": [signal]}


def test_highest_severity_returns_largest_rank():
    signals = [
        OperationSignal("docs-drift", "medium", "docs", datetime.now(timezone.utc)),
        OperationSignal("release-blocker", "critical", "release", datetime.now(timezone.utc)),
    ]

    assert highest_severity(signals) == "critical"


def test_summarize_signals_for_handoff_rolls_owner_severity_and_count():
    signals = [
        OperationSignal("flake", "low", "qa", datetime.now(timezone.utc)),
        OperationSignal("handoff", "high", "   ", datetime.now(timezone.utc)),
    ]

    summary = summarize_signals_for_handoff(signals, fallback_owner="release")

    assert summary.highest_severity == "high"
    assert summary.owners == ("qa", "release")
    assert summary.signal_count == 2


def test_build_release_marker_defaults_blank_channel_to_internal():
    marker = build_release_marker("2026.05.30", "   ")

    assert marker.startswith("2026.05.30-internal-")


def test_parse_release_marker_round_trips_values():
    marker = parse_release_marker("2026.05.30-internal-202605301145")

    assert marker.version == "2026.05.30"
    assert marker.channel == "internal"
    assert marker.observed_at == datetime(2026, 5, 30, 11, 45, tzinfo=timezone.utc)


def test_parse_release_marker_rejects_short_timestamps():
    with pytest.raises(ValueError, match="timestamp"):
        parse_release_marker("2026.05.30-internal-20260530114")
