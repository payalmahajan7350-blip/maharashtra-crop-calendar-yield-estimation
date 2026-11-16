"""Validate the frozen final analysis-ready cohort without altering it."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "processed_modeling_data.csv"
KEYS = ["Crop", "District", "Crop_Year"]


def main():
    df = pd.read_csv(DATA)
    assert df.shape == (1980, 131)
    assert not df.duplicated(KEYS).any()
    assert df.Crop.nunique() == 10
    assert df.groupby(["Crop", "District"]).ngroups == 118
    assert (int(df.Crop_Year.min()), int(df.Crop_Year.max())) == (2003, 2022)
    assert df.Split.value_counts().to_dict() == {
        "Training": 1346, "Validation": 354, "Test": 280
    }
    assert set(df.loc[df.District.eq("Palghar"), "Crop_Year"]) == {
        2017, 2018, 2019, 2021, 2022
    }
    assert df.notna().all().all()
    print("Validated final observed-only cohort: 1,980 rows; 118 series; 280 test rows")


if __name__ == "__main__":
    main()
