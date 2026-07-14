DEFAULT_OWNER = "engineering-ops"


def normalize_delivery_owner(owner: str | None) -> str:
    """Return the routing key used by delivery workflows."""
    normalized = (owner or "").strip().lower()
    return normalized or DEFAULT_OWNER


def delivery_summary(record: dict, *, include_source: bool = False) -> dict:
    """Return the stable summary fields currently exposed to callers."""
    summary = {
        "owner": normalize_delivery_owner(record.get("owner")),
        "status": record["status"],
    }
    if include_source:
        summary["source"] = record.get("source") or "unknown"
    return summary
