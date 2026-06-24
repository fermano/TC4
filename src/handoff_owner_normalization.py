def normalize_handoff_owner(owner):
    normalized = owner.strip()
    return normalized or None


def normalized_owner_rows(rows):
    return [
        {**row, "owner": normalize_handoff_owner(row.get("owner", ""))}
        for row in rows
    ]
