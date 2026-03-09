"""Load AHP-TOPSIS payloads from JSON"""

from typing import Any


def _tuple_key_dict_from_json_dict(d: dict[str, Any]) -> dict[tuple, float]:
    """Convert `"A | B"` string keys to `(A, B)` tuple keys."""
    out = {}
    for k, v in d.items():
        if isinstance(k, str) and " | " in k:
            a, b = k.split(" | ", 1)
            key = (a.strip(), b.strip())
        else:
            key = k
        out[key] = float(v) if v is not None else v
    return out


def load_payload_from_dict(data: dict[str, Any]) -> dict[str, Any]:
    """Build a payload for `quick_recommend()` from a JSON"""
    payload = {
        "criteria_comparisons": _tuple_key_dict_from_json_dict(
            data["criteria_comparisons"]
        ),
        "subcriteria_comparisons": {},
    }
    for criterion, pairs in data["subcriteria_comparisons"].items():
        payload["subcriteria_comparisons"][criterion] = _tuple_key_dict_from_json_dict(
            pairs
        )
    return payload
