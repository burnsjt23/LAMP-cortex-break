"""Hometime feature based on significant locations."""
from typing import Any, Dict
from ..primary.significant_locations import significant_locations


def hometime(data: Any, *, start: int | None = None, end: int | None = None) -> Dict:
    """Return time spent in the most visited location."""
    siglocs = significant_locations(data, start=start, end=end)
    if not siglocs["data"]:
        value = None
    else:
        value = siglocs["data"][0]["duration"]
    return {"timestamp": start if start is not None else 0, "value": value}
