"""Owner-based filtering for delivery workflow records."""

from __future__ import annotations

from collections.abc import Iterable, Sequence

from src.ticket_workflow_seed import normalize_delivery_owner


def filter_delivery_records(
    records: Iterable[dict],
    owners: Sequence[str] | None = None,
) -> list[dict]:
    """Return records whose canonical owner is in the selection.

    ``owners=None`` means no filtering. An explicitly empty selection
    selects no owners and therefore returns an empty list. Input record
    order is always preserved.
    """
    record_list = list(records)
    if owners is None:
        return record_list
    selected = {normalize_delivery_owner(owner) for owner in owners}
    return [
        record
        for record in record_list
        if normalize_delivery_owner(record.get("owner")) in selected
    ]
