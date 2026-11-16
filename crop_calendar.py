"""Study-defined half-open, equal-elapsed-duration crop-calendar intervals."""

from datetime import datetime
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
CALENDAR = ROOT / "data" / "crop_calendar.csv"


def phase_boundaries(crop, crop_year):
    table = pd.read_csv(CALENDAR).set_index("Crop")
    record = table.loc[crop]
    start = datetime(crop_year, int(record.Start_Month), int(record.Start_Day))
    end_year = crop_year + int(record.Cross_Year)
    end = datetime(end_year, int(record.End_Month), int(record.End_Day))
    duration = end - start
    return [start + duration * (i / 5) for i in range(6)]


def phase_for_timestamp(crop, crop_year, timestamp):
    """Return P1...P5 for start <= t < end, otherwise None."""
    t = pd.Timestamp(timestamp).to_pydatetime()
    bounds = phase_boundaries(crop, crop_year)
    for i in range(5):
        if bounds[i] <= t < bounds[i + 1]:
            return f"P{i + 1}"
    return None
