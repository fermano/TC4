import pytest

from src.intake_service import (
    extract_release_marker,
    filter_handoff_rows,
    resolve_retry_budget,
)


def test_retry_budget_uses_default_when_omitted() -> None:
    assert resolve_retry_budget(None, 3) == 3


def test_retry_budget_accepts_positive_override() -> None:
    assert resolve_retry_budget(2, 3) == 2


def test_retry_budget_accepts_zero_override() -> None:
    assert resolve_retry_budget(0, 3) == 0


def test_retry_budget_rejects_negative_override() -> None:
    with pytest.raises(ValueError, match="zero or greater"):
        resolve_retry_budget(-1, 3)


def test_handoff_rows_keep_input_order() -> None:
    rows = [
        {"owner": "platform", "severity": "high", "summary": "Queue delay"},
        {"owner": "support", "severity": "low", "summary": "Copy cleanup"},
    ]

    assert filter_handoff_rows(rows) == rows


def test_handoff_rows_filter_by_minimum_severity_in_input_order() -> None:
    rows = [
        {"owner": "platform", "severity": "high", "summary": "Queue delay"},
        {"owner": "support", "severity": "unknown", "summary": "Needs triage"},
        {"owner": "release", "severity": "critical", "summary": "Release blocked"},
        {"owner": "docs", "severity": "low", "summary": "Copy cleanup"},
    ]

    assert filter_handoff_rows(rows, minimum_severity="high") == [rows[0], rows[2]]


def test_handoff_rows_reject_unknown_minimum_severity() -> None:
    with pytest.raises(ValueError, match="unknown minimum severity"):
        filter_handoff_rows([], minimum_severity="urgent")


def test_handoff_rows_filter_by_normalized_owner_in_input_order() -> None:
    rows = [
        {"owner": "Engineering Ops", "severity": "low", "summary": "First"},
        {"owner": "support", "severity": "critical", "summary": "Second"},
        {"owner": "engineering-ops", "severity": "high", "summary": "Third"},
    ]

    assert filter_handoff_rows(rows, owner=" engineering OPS! ") == [rows[0], rows[2]]


def test_handoff_rows_combine_owner_and_minimum_severity_filters() -> None:
    rows = [
        {"owner": "release", "severity": "low", "summary": "First"},
        {"owner": "support", "severity": "critical", "summary": "Second"},
        {"owner": "Release", "severity": "high", "summary": "Third"},
    ]

    assert filter_handoff_rows(rows, owner="release", minimum_severity="high") == [rows[2]]


def test_handoff_rows_return_empty_list_when_owner_does_not_match() -> None:
    rows = [{"owner": "support", "severity": "high", "summary": "Queue delay"}]

    assert filter_handoff_rows(rows, owner="release") == []


def test_handoff_rows_filter_blank_owners_as_unassigned() -> None:
    rows = [
        {"owner": "support", "severity": "high", "summary": "Named owner"},
        {"owner": "   ", "severity": "low", "summary": "Copied blank owner"},
    ]

    assert filter_handoff_rows(rows, owner="") == [rows[1]]


def test_release_marker_trims_surrounding_whitespace() -> None:
    assert extract_release_marker("  20260530-rc2  ") == "20260530-rc2"


def test_release_marker_accepts_case_insensitive_support_prefix() -> None:
    assert extract_release_marker("  ReLeAsE: 20260530-rc2  ") == "20260530-rc2"


def test_release_marker_rejects_empty_support_prefix() -> None:
    with pytest.raises(ValueError, match="must include a value"):
        extract_release_marker(" release:   ")
