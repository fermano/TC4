"""Helpers used by support intake and release coordination paths."""

from __future__ import annotations

import re
from collections.abc import Iterable
from typing import TypedDict


class HandoffRow(TypedDict):
    owner: str
    severity: str
    summary: str


SEVERITY_RANK = {"low": 1, "medium": 2, "high": 3, "critical": 4}
RELEASE_MARKER_PREFIX_RE = re.compile(r"^release:\s*", re.IGNORECASE)


def resolve_retry_budget(requested: int | None, default: int) -> int:
    """Return the configured retry count unless a request overrides it."""
    return default if requested is None else requested


def filter_handoff_rows(
    rows: Iterable[HandoffRow],
    *,
    minimum_severity: str | None = None,
) -> list[HandoffRow]:
    """Return qualifying handoff rows in the order copied from support notes."""
    row_list = list(rows)
    if minimum_severity is None:
        return row_list

    try:
        minimum_rank = SEVERITY_RANK[minimum_severity]
    except KeyError as exc:
        raise ValueError(f"unknown minimum severity: {minimum_severity}") from exc

    return [row for row in row_list if SEVERITY_RANK.get(row["severity"], 0) >= minimum_rank]


def extract_release_marker(note: str) -> str:
    """Normalize a plain or support-prefixed release marker."""
    marker = note.strip()
    if RELEASE_MARKER_PREFIX_RE.match(marker):
        marker = RELEASE_MARKER_PREFIX_RE.sub("", marker, count=1).strip()
        if not marker:
            raise ValueError("prefixed release marker must include a value")

    return marker
