from src.rc104_harbor_void_export import build_export_row


def test_partner_void_reason_alias_suppresses_row():
    row = build_export_row(
        {"tenant": "harbor", "shipment_id": "ship-614", "voidReason": "carrier-reversal"},
        {"route": "ferry", "audit_key": "hb-a"},
    )

    assert row["status"] == "voided"
    assert row["include_in_export"] is False
    assert row["void_reason"] == "carrier-reversal"
