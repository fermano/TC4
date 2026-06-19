def serialize_handoff_filter(filter_state):
    return {
        "owners": list(filter_state.get("owners", [])),
        "minimum_severity": filter_state.get("minimum_severity"),
    }


def load_handoff_filter(payload):
    return {
        "owners": list(payload.get("owners", [])),
        "minimum_severity": payload.get("minimum_severity"),
    }
