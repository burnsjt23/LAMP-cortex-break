"""Compute periods when the screen was active (unlocked)."""
from typing import Any, List, Dict
from ..raw.device_state import device_state


def screen_active(data: Any) -> List[Dict[str, int]]:
    """Return intervals during which the device was unlocked."""
    records = device_state(data)
    intervals: List[Dict[str, int]] = []
    unlocked = False
    start = 0
    for r in records:
        rep = r["representation"]
        ts = int(r["timestamp"])
        if not unlocked and rep == "unlocked":
            unlocked = True
            start = ts
        elif unlocked and rep in {"locked", "screen_off"}:
            intervals.append({"start": start, "end": ts})
            unlocked = False
    if unlocked and records:
        intervals.append({"start": start, "end": int(records[-1]["timestamp"])})
    return intervals
