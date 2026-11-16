"""Check frozen, final-test MAE/RMSE without fitting or selecting models."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]


def main():
    pred = pd.read_csv(ROOT / "data" / "frozen_test_predictions.csv")
    reported = pd.read_csv(ROOT / "data" / "reported_crop_metrics.csv").set_index("Crop")
    assert len(pred) == 280 and pred.Crop.nunique() == 10
    for crop, group in pred.groupby("Crop"):
        error = group.Actual.to_numpy() - group.Predicted.to_numpy()
        mae = np.abs(error).mean()
        rmse = np.sqrt(np.square(error).mean())
        assert np.isclose(mae, reported.loc[crop, "MAE"], atol=1e-9)
        assert np.isclose(rmse, reported.loc[crop, "RMSE"], atol=1e-9)
    print("Frozen MAE/RMSE verified for all ten crops")


if __name__ == "__main__":
    main()
