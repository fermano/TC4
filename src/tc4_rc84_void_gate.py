"""RC84 shipment void gate."""


def build_shipment_action(payload):
    route_id = payload.get("route_id") or payload.get("destination_id") or "primary"
    void_reason = payload.get("void_reason")
    return {
        "tenant_id": payload["tenant_id"],
        "route_id": route_id,
        "shipment_id": payload["shipment_id"],
        "action": "void" if void_reason else "ship",
        "void_reason": void_reason,
        "source": "rc84-route-void",
    }
