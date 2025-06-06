"""Raw GPS events."""
from typing import Any, List, Dict
from ..utils.loading import load_data


def gps(data: Any) -> List[Dict]:
    """Return GPS events sorted by timestamp."""
    records = load_data(data)
    required = {"timestamp", "latitude", "longitude"}
    for r in records:
        if not required.issubset(r.keys()):
            raise ValueError("GPS data missing required columns.")
    records.sort(key=lambda x: int(x["timestamp"]))
    return [{k: r[k] for k in required} for r in records]
