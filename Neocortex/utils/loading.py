import os
import json
import csv
from typing import Any, List, Dict


def load_data(source: Any) -> List[Dict]:
    """Load data from CSV/JSON path, JSON string, or list of dictionaries."""
    if isinstance(source, list):
        return list(source)
    if isinstance(source, dict):
        return [source]
    if isinstance(source, str):
        source = source.strip()
        if os.path.isfile(source):
            ext = os.path.splitext(source)[1].lower()
            if ext == ".csv":
                with open(source, newline="") as f:
                    return list(csv.DictReader(f))
            if ext == ".json":
                with open(source) as f:
                    return json.load(f)
        return json.loads(source)
    raise ValueError("Unsupported data source")
