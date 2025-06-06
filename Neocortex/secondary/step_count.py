"""Daily step count aggregate."""
from typing import Any, List, Dict
from ..raw.steps import steps

MS_IN_DAY = 86400000


def step_count(data: Any, *, start: int | None = None, end: int | None = None,
               resolution: int = MS_IN_DAY) -> List[Dict[str, int]]:
    """Aggregate steps into bins of ``resolution`` milliseconds."""
    records = steps(data)
    if not records:
        return []
    timestamps = [int(r["timestamp"]) for r in records]
    if start is None:
        start = min(timestamps)
    if end is None:
        end = max(timestamps) + 1
    if start > end:
        raise ValueError("'start' must be <= 'end'")

    bins = list(range(start, end, resolution))
    results: List[Dict[str, int]] = []
    for b in bins:
        bin_end = b + resolution
        value = sum(int(r["value"]) for r in records if b <= int(r["timestamp"]) < bin_end)
        results.append({"timestamp": b, "value": value})
    return results
