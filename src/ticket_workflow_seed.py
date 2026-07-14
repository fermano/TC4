DEFAULT_OWNER = "engineering-ops"


def normalize_delivery_owner(owner: str | None) -> str:
    """Return the routing key used by delivery workflows."""
    normalized = " ".join((owner or "").split()).lower()
    return normalized or DEFAULT_OWNER


def delivery_summary(record: dict, *, include_source: bool = False) -> dict:
    """Return the stable summary fields currently exposed to callers."""
    summary = {
        "owner": normalize_delivery_owner(record.get("owner")),
        "status": record["status"],
    }
    if include_source:
        source = (record.get("source") or "").strip()
        summary["source"] = source or "unknown"
    return summary
