"""Optional SHAP reanalysis of independently reproduced final configurations.

This does not reproduce the frozen manuscript SHAP table or modify model selection.
Run only after code/modeling/reproduce_models.py has written selected_models.csv.
"""

from pathlib import Path
import sys

import numpy as np
import pandas as pd
import shap
from sklearn.base import clone

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code" / "modeling"))
from reproduce_models import TARGET, models  # noqa: E402


def main():
    configs_path = ROOT / "reproduced_results" / "selected_models.csv"
    if not configs_path.exists():
        raise SystemExit("Run code/modeling/reproduce_models.py first.")
    data = pd.read_csv(ROOT / "data" / "processed_modeling_data.csv")
    configs = pd.read_csv(configs_path)
    rows = []
    for config in configs.itertuples(index=False):
        features = config.Selected_Features.split("; ")
        crop = data[data.Crop.eq(config.Crop)]
        refit = crop[~crop.Split.eq("Test")]
        test = crop[crop.Split.eq("Test")]
        model = clone(models()[config.Model])
        model.fit(refit[features], refit[TARGET])
        if config.Model == "Linear Regression":
            values = shap.LinearExplainer(model, refit[features]).shap_values(test[features])
        else:
            values = shap.TreeExplainer(model).shap_values(test[features])
        importance = np.abs(np.asarray(values)).mean(axis=0)
        rows.extend(
            {"Crop": config.Crop, "Feature": feature, "Mean_Absolute_SHAP": float(value)}
            for feature, value in zip(features, importance)
        )
    pd.DataFrame(rows).to_csv(ROOT / "reproduced_results" / "optional_shap.csv", index=False)


if __name__ == "__main__":
    main()
