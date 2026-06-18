"""Helpers used by support intake and release coordination paths."""

from __future__ import annotations

import re
from collections.abc import Iterable
from typing import TypedDict


class HandoffRow(TypedDict):
    owner: str
    severity: str
    summary: str


class HandoffCounts(TypedDict):
    total: int
    by_owner: dict[str, int]
    by_severity: dict[str, int]


SEVERITY_RANK = {"low": 1, "medium": 2, "high": 3, "critical": 4}
RELEASE_MARKER_PREFIX_RE = re.compile(r"^release:\s*", re.IGNORECASE)
OWNER_SLUG_RE = re.compile(r"[^a-z0-9]+")


def normalize_owner(owner: str) -> str:
    """Return the routing key used for copied handoff owners."""
    cleaned = OWNER_SLUG_RE.sub("-", owner.strip().lower()).strip("-")
    return cleaned or "unassigned"


def resolve_retry_budget(requested: int | None, default: int) -> int:
    """Return the configured retry count unless a request overrides it."""
    if requested is None:
        return default
    if requested < 0:
        raise ValueError("retry budget must be zero or greater")
    return requested


def filter_handoff_rows(
    rows: Iterable[HandoffRow],
    *,
    minimum_severity: str | None = None,
    owner: str | None = None,
) -> list[HandoffRow]:
    """Return qualifying handoff rows in the order copied from support notes."""
    row_list = list(rows)
    if minimum_severity is not None:
        try:
            minimum_rank = SEVERITY_RANK[minimum_severity]
        except KeyError as exc:
            raise ValueError(f"unknown minimum severity: {minimum_severity}") from exc
        row_list = [
            row for row in row_list if SEVERITY_RANK.get(row["severity"], 0) >= minimum_rank
        ]

    if owner is not None:
        owner_key = normalize_owner(owner)
        row_list = [row for row in row_list if normalize_owner(row["owner"]) == owner_key]

    return row_list


def summarize_handoff_rows(rows: Iterable[HandoffRow]) -> HandoffCounts:
    """Count handoff rows by normalized owner and recognized severity."""
    total = 0
    by_owner: dict[str, int] = {}
    by_severity: dict[str, int] = {}

    for row in rows:
        total += 1

        owner_key = normalize_owner(row["owner"])
        by_owner[owner_key] = by_owner.get(owner_key, 0) + 1

        severity_key = row["severity"].strip().lower()
        if severity_key in SEVERITY_RANK:
            by_severity[severity_key] = by_severity.get(severity_key, 0) + 1

    return {
        "total": total,
        "by_owner": by_owner,
        "by_severity": by_severity,
    }


def extract_release_marker(note: str) -> str:
    """Normalize a plain or support-prefixed release marker."""
    marker = note.strip()
    if RELEASE_MARKER_PREFIX_RE.match(marker):
        marker = RELEASE_MARKER_PREFIX_RE.sub("", marker, count=1).strip()
        if not marker:
            raise ValueError("prefixed release marker must include a value")

    return marker
