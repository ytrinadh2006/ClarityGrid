import json

def export_diagnostics_json(summary: dict) -> str:
    return json.dumps(summary, indent=2, default=str)
