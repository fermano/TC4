def drop_blank_owner_rows(rows):
    return [row for row in rows if row.get("owner", "").strip()]
