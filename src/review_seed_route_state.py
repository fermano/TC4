"""Seed-only helper for the requested regression."""

def final_route_state(events):
    return "voided" if "voided" in events else "active"
