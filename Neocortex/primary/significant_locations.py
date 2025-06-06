"""Simple significant location extraction."""
from typing import Any, Dict, Tuple
from ..raw.gps import gps


def _cluster_key(lat: float, lon: float) -> Tuple[float, float]:
    """Return a rounded cluster key."""
    return (round(lat, 3), round(lon, 3))


def significant_locations(data: Any, *, start: int | None = None, end: int | None = None) -> Dict:
    """Group GPS points by approximate location and compute duration and proportion."""
    records = gps(data)
    if not records:
        return {"data": [], "has_raw_data": 0}

    records.sort(key=lambda r: int(r["timestamp"]))

    if start is None:
        start = int(records[0]["timestamp"])
    if end is None:
        end = int(records[-1]["timestamp"])

    durations: dict[Tuple[float, float], int] = {}
    for i, rec in enumerate(records):
        ts = int(rec["timestamp"])
        key = _cluster_key(float(rec["latitude"]), float(rec["longitude"]))
        next_ts = end if i == len(records) - 1 else int(records[i + 1]["timestamp"])
        seg_start = max(ts, start)
        seg_end = min(next_ts, end)
        if seg_end <= seg_start:
            continue
        durations[key] = durations.get(key, 0) + (seg_end - seg_start)

    total = sum(durations.values())
    clusters = []
    for idx, (key, dur) in enumerate(sorted(durations.items(), key=lambda x: x[1], reverse=True)):
        proportion = dur / total if total else 0
        clusters.append({
            "latitude": key[0],
            "longitude": key[1],
            "radius": 0,
            "proportion": proportion,
            "duration": dur,
            "rank": idx,
        })
    return {"data": clusters, "has_raw_data": 1}
