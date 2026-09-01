def resolve_partner_value(payload, default=""):
    value = payload.get("void_reason")
    if value is None:
        value = payload.get("voidReason")
    return default if value in (None, "") else value
