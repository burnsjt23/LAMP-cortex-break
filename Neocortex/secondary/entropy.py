"""Entropy feature based on significant locations."""
from typing import Any, Dict
import math
from ..primary.significant_locations import significant_locations


def entropy(data: Any, *, start: int | None = None, end: int | None = None) -> Dict:
    """Return entropy of time spent across significant locations."""
    siglocs = significant_locations(data, start=start, end=end)
    if not siglocs["data"]:
        value = None
    else:
        value = -sum(
            loc["proportion"] * math.log(loc["proportion"])
            for loc in siglocs["data"]
            if 0 < loc["proportion"] <= 1
        )
    return {"timestamp": start if start is not None else 0, "value": value}
