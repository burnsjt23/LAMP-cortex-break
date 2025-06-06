"""Raw device state events."""
from typing import Any, List, Dict
from ..utils.loading import load_data


def device_state(data: Any) -> List[Dict]:
    """Return device state events sorted by timestamp."""
    records = load_data(data)
    for r in records:
        if "timestamp" not in r or "representation" not in r:
            raise ValueError(
                "Device state data must contain 'timestamp' and 'representation'."
            )
    records.sort(key=lambda x: int(x["timestamp"]))
    return records
