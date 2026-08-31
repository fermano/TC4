from src.tc4_rc84_void_gate import ARTIFACT_SCHEMA, build_shipment_action


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
    assert row["artifact_schema"] == ARTIFACT_SCHEMA
    assert row["route_action_key"] == "cold-chain:ship-642:void"


def test_missing_reason_keeps_ship_action():
    row = build_shipment_action({"tenant_id": "harbor", "route_id": "ground", "shipment_id": "ship-104"})
    assert row["action"] == "ship"


def test_camel_case_void_reason_voids_route_row():
    row = build_shipment_action({
        "tenant_id": "harbor",
        "route_id": "cold-chain",
        "shipment_id": "ship-642",
        "voidReason": "customer-cancelled",
    })
    assert row["action"] == "void"
    assert row["void_reason"] == "customer-cancelled"
    assert row["route_id"] == "cold-chain"
    assert row["source"] == "rc84-route-void"
    assert row["artifact_schema"] == ARTIFACT_SCHEMA
    assert row["route_action_key"] == "cold-chain:ship-642:void"


def test_snake_case_reason_takes_precedence_over_camel_case():
    row = build_shipment_action({
        "tenant_id": "harbor",
        "route_id": "cold-chain",
        "shipment_id": "ship-642",
        "void_reason": "damaged-goods",
        "voidReason": "customer-cancelled",
    })
    assert row["action"] == "void"
    assert row["void_reason"] == "damaged-goods"


def test_blank_reason_does_not_void():
    row = build_shipment_action({
        "tenant_id": "harbor",
        "route_id": "cold-chain",
        "shipment_id": "ship-642",
        "void_reason": "  ",
    })
    assert row["action"] == "ship"
    assert row["void_reason"] is None
    assert row["route_action_key"] == "cold-chain:ship-642:ship"


def test_blank_camel_case_reason_does_not_void():
    row = build_shipment_action({
        "tenant_id": "harbor",
        "route_id": "cold-chain",
        "shipment_id": "ship-642",
        "voidReason": "   ",
    })
    assert row["action"] == "ship"
    assert row["void_reason"] is None
