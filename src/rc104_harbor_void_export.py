def build_export_row(payload, route_defaults):
    reason = payload.get("void_reason")
    voided = bool(reason)
    return {
        "tenant": payload["tenant"],
        "shipment_id": payload["shipment_id"],
        "route": route_defaults["route"],
        "status": "voided" if voided else "active",
        "include_in_export": not voided,
        "void_reason": reason or "",
        "artifact_stage": route_defaults.get("artifact_stage", "rc104"),
        "audit_key": route_defaults.get("audit_key", "unset"),
    }
