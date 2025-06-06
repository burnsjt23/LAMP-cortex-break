"""Raw step count events."""
from typing import Any, List, Dict
from ..utils.loading import load_data


def steps(data: Any) -> List[Dict]:
    """Return step events sorted by timestamp."""
    records = load_data(data)
    for r in records:
        if "timestamp" not in r or "value" not in r:
            raise ValueError("Steps data must contain 'timestamp' and 'value'.")
    records.sort(key=lambda x: int(x["timestamp"]))
    return records
