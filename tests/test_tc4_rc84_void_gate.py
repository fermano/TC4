from src.tc4_rc84_void_gate import build_shipment_action


def test_void_gate_uses_route_shape():
    row = build_shipment_action({
        "tenant_id": "harbor",
        "route_id": "cold-chain",
        "shipment_id": "ship-642",
        "void_reason": "duplicate-label",
    })
    assert row["route_id"] == "cold-chain"
    assert row["action"] == "void"
    assert row["source"] == "rc84-route-void"


def test_missing_reason_keeps_ship_action():
    row = build_shipment_action({"tenant_id": "harbor", "route_id": "ground", "shipment_id": "ship-104"})
    assert row["action"] == "ship"
