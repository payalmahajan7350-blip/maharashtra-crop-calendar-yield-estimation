"""Smoke tests for the published analytical calendar only."""

import sys
import unittest
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code" / "feature_engineering"))

from crop_calendar import phase_boundaries, phase_for_timestamp  # noqa: E402


class CalendarTests(unittest.TestCase):
    def test_five_half_open_intervals(self):
        bounds = phase_boundaries("Soyabean", 2020)
        self.assertEqual(len(bounds), 6)
        self.assertEqual(bounds[0], datetime(2020, 6, 15))
        self.assertEqual(bounds[-1], datetime(2020, 10, 31))
        for i in range(5):
            self.assertEqual(phase_for_timestamp("Soyabean", 2020, bounds[i]), f"P{i + 1}")
        self.assertIsNone(phase_for_timestamp("Soyabean", 2020, bounds[-1]))

    def test_cross_year_window(self):
        bounds = phase_boundaries("Cotton", 2020)
        self.assertEqual(bounds[0], datetime(2020, 6, 1))
        self.assertEqual(bounds[-1], datetime(2021, 1, 31))


if __name__ == "__main__":
    unittest.main()
