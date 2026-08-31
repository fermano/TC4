def _pick_void_reason(payload):
    if "voidReason" in payload:
        return payload["voidReason"]
    return payload.get("void_reason")


def build_export_row(payload, route_defaults):
    reason = _pick_void_reason(payload)
    voided = reason is not None and reason != ""
    return {
        "tenant": payload["tenant"],
        "shipment_id": payload["shipment_id"],
        "route": route_defaults["route"],
        "status": "voided" if voided else "active",
        "include_in_export": not voided,
        "void_reason": reason or "",
    }
