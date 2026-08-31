from src.rc104_harbor_void_export import build_export_row


def test_active_row_is_included_when_no_void_reason():
    row = build_export_row(
        {"tenant": "harbor", "shipment_id": "ship-614"},
        {"route": "ferry", "artifact_stage": "candidate", "audit_key": "hb-a", "release_channel": "rc104-final"},
    )

    assert row["status"] == "active"
    assert row["include_in_export"] is True
    assert row["artifact_stage"] == "candidate"
    assert row["audit_key"] == "hb-a"
    assert row["release_channel"] == "rc104-final"


def test_snake_void_reason_suppresses_export_row():
    row = build_export_row(
        {"tenant": "harbor", "shipment_id": "ship-615", "void_reason": "duplicate-scan"},
        {"route": "ferry"},
    )

    assert row["status"] == "voided"
    assert row["include_in_export"] is False
    assert row["void_reason"] == "duplicate-scan"
    assert row["release_channel"] == "candidate"


def test_partner_void_reason_alias_suppresses_row_and_keeps_release_fields():
    row = build_export_row(
        {"tenant": "harbor", "shipment_id": "ship-614", "voidReason": "carrier-reversal"},
        {"route": "ferry", "artifact_stage": "candidate", "audit_key": "hb-a", "release_channel": "rc104-final"},
    )

    assert row["status"] == "voided"
    assert row["include_in_export"] is False
    assert row["void_reason"] == "carrier-reversal"
    assert row["artifact_stage"] == "candidate"
    assert row["audit_key"] == "hb-a"
    assert row["release_channel"] == "rc104-final"


def test_snake_void_reason_takes_precedence_over_partner_alias():
    row = build_export_row(
        {
            "tenant": "harbor",
            "shipment_id": "ship-617",
            "void_reason": "duplicate-scan",
            "voidReason": "carrier-reversal",
        },
        {"route": "ferry"},
    )

    assert row["status"] == "voided"
    assert row["void_reason"] == "duplicate-scan"


def test_empty_snake_void_reason_keeps_active_row():
    row = build_export_row(
        {"tenant": "harbor", "shipment_id": "ship-616", "void_reason": ""},
        {"route": "ferry", "audit_key": "hb-a"},
    )

    assert row["status"] == "active"
    assert row["include_in_export"] is True
    assert row["audit_key"] == "hb-a"


def test_whitespace_partner_void_reason_keeps_active_row():
    row = build_export_row(
        {"tenant": "harbor", "shipment_id": "ship-618", "voidReason": "   "},
        {"route": "ferry"},
    )

    assert row["status"] == "active"
    assert row["include_in_export"] is True
    assert row["void_reason"] == ""
