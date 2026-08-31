"""RC84 shipment void gate."""

ARTIFACT_SCHEMA = "rc84.void.v2"


def build_shipment_action(payload):
    route_id = payload.get("route_id") or payload.get("destination_id") or "primary"
    void_reason = payload.get("void_reason")
    action = "void" if void_reason else "ship"
    return {
        "tenant_id": payload["tenant_id"],
        "route_id": route_id,
        "shipment_id": payload["shipment_id"],
        "action": action,
        "void_reason": void_reason,
        "source": "rc84-route-void",
        "artifact_schema": ARTIFACT_SCHEMA,
        "route_action_key": f"{route_id}:{payload['shipment_id']}:{action}",
    }
