from src.tc4_rc84_void_gate import build_shipment_action


def test_camel_void_reason_sets_void_action():
    row = build_shipment_action({
        "tenant_id": "harbor",
        "destination_id": "cold-chain",
        "shipment_id": "ship-642",
        "voidReason": "customer-cancelled",
    })
    assert row["action"] == "void"
    assert row["void_reason"] == "customer-cancelled"
