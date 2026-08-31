def _void_reason(payload):
    value = payload.get("void_reason")
    if value is None:
        value = payload.get("voidReason")
    if isinstance(value, str):
        value = value.strip()
    return value or None


def build_export_row(payload, route_defaults):
    reason = _void_reason(payload)
    voided = reason is not None
    return {
        "tenant": payload["tenant"],
        "shipment_id": payload["shipment_id"],
        "route": route_defaults["route"],
        "status": "voided" if voided else "active",
        "include_in_export": not voided,
        "void_reason": reason or "",
        "artifact_stage": route_defaults.get("artifact_stage", "rc104"),
        "audit_key": route_defaults.get("audit_key", "unset"),
        "release_channel": route_defaults.get("release_channel", "candidate"),
    }
