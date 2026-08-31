"""Prototype void gate from before RC84 route rows."""


def _reason(payload):
    value = payload.get("void_reason")
    if value is None:
        value = payload.get("voidReason")
    if isinstance(value, str):
        value = value.strip()
    return value or None


def build_shipment_action(payload):
    reason = _reason(payload)
    return {
        "tenant_id": payload["tenant_id"],
        "destination_id": payload.get("destination_id") or payload.get("route_id") or "primary",
        "shipment_id": payload["shipment_id"],
        "action": "void" if reason else "ship",
        "void_reason": reason,
        "source": "mainline-void-reason",
    }
