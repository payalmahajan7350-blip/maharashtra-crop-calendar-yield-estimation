"""Chronological validation/refit model comparison from the final processed cohort.

This script is supplied for author-side reproduction after dependency installation.
Running it may show small package-version differences from frozen reported values.
It is not executed as part of the editorial Batch 3 changes.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from catboost import CatBoostRegressor

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "processed_modeling_data.csv"
OUTPUT = ROOT / "reproduced_results"
TARGET = "Yield (Tonne/Hectare)"
TEMPORAL = ["Crop_Year", "Time_Index", "Yield_Lag_1", "Yield_Lag_2",
            "Yield_Lag_3", "Yield_RollingMean_3", "Yield_RollingStd_3"]
WEATHER_TOKENS = ["CLOUD", "CUM_RAINFALL", "CUM_RAINY", "GWETROOT",
                  "RAINFALL", "RAINY", "RH2M", "SW_DWN", "T2M", "WS10M"]
SATELLITE_TOKENS = ["CUM_EVI", "CUM_NDVI", "EVI", "LST", "NDVI"]
CANDIDATE_ENV_K = [5, 7, 10, 12, 15, 17, 20, 22, 25, 27, 30,
                   35, 40, 45, 50, 60, 70, 80, 90, 100, 110, 120]


def rf():
    return RandomForestRegressor(n_estimators=300, max_depth=8,
                                 min_samples_leaf=3, random_state=42, n_jobs=-1)


def models():
    return {
        "Linear Regression": LinearRegression(),
        "Random Forest": rf(),
        "CatBoost": CatBoostRegressor(iterations=300, learning_rate=0.03,
                                      depth=4, loss_function="RMSE", verbose=0,
                                      random_state=42),
    }


def rmse(actual, predicted):
    return float(np.sqrt(mean_squared_error(actual, predicted)))


def candidate_ks(max_k):
    grid = [k for k in CANDIDATE_ENV_K if k <= max_k]
    if max_k <= 12:
        grid.extend(range(1, max_k + 1))
    grid.append(max_k)
    return sorted(set(grid))


def select_features(train, validation, env_pool):
    if not env_pool:
        return TEMPORAL.copy(), []
    ranking_model = rf()
    all_features = TEMPORAL + env_pool
    ranking_model.fit(train[all_features], train[TARGET])
    ranking = pd.Series(ranking_model.feature_importances_, index=all_features)
    ranked_env = ranking.loc[env_pool].sort_values(ascending=False).index.tolist()
    trials = []
    for k in candidate_ks(len(ranked_env)):
        features = TEMPORAL + ranked_env[:k]
        model = rf()
        model.fit(train[features], train[TARGET])
        trials.append((k, rmse(validation[TARGET], model.predict(validation[features]))))
    minimum = min(error for _, error in trials)
    selected_k = next(k for k, error in trials if error <= 1.01 * minimum)
    return TEMPORAL + ranked_env[:selected_k], trials


def run():
    data = pd.read_csv(DATA)
    assert len(data) == 1980 and data.notna().all().all()
    numeric = [c for c in data.select_dtypes(include=[np.number]).columns
               if c not in TEMPORAL + [TARGET]]
    weather = sorted(c for c in numeric if any(token in c for token in WEATHER_TOKENS))
    satellite = sorted(c for c in numeric if any(token in c for token in SATELLITE_TOKENS))
    groups = {"Temporal": [], "Temporal + Weather": weather,
              "Temporal + Weather + Satellite": sorted(set(weather + satellite))}
    rows, predictions = [], []
    for crop, crop_data in data.groupby("Crop"):
        train = crop_data[crop_data.Split.eq("Training")]
        val = crop_data[crop_data.Split.eq("Validation")]
        refit = crop_data[~crop_data.Split.eq("Test")]
        test = crop_data[crop_data.Split.eq("Test")]
        candidates = []
        for group, environmental in groups.items():
            features, curve = select_features(train, val, environmental)
            for name, template in models().items():
                model = clone(template)
                model.fit(train[features], train[TARGET])
                candidates.append((rmse(val[TARGET], model.predict(val[features])),
                                   group, name, template, features, curve))
        # No test prediction is made until validation has selected one configuration.
        best_error, group, name, template, features, curve = min(candidates, key=lambda x: x[0])
        model = clone(template)
        model.fit(refit[features], refit[TARGET])
        pred = model.predict(test[features])
        rows.append({"Crop": crop, "Feature_Group": group, "Model": name,
                     "Selected_Feature_Count": len(features), "Validation_RMSE": best_error,
                     "Test_RMSE": rmse(test[TARGET], pred), "N_Test": len(test),
                     "Selected_Features": "; ".join(features)})
        for record, estimate in zip(test.itertuples(index=False), pred):
            predictions.append({"Crop": crop, "District": record.District,
                                "Crop_Year": record.Crop_Year, "Predicted": estimate})
    OUTPUT.mkdir(exist_ok=True)
    pd.DataFrame(rows).to_csv(OUTPUT / "selected_models.csv", index=False)
    pd.DataFrame(predictions).to_csv(OUTPUT / "test_predictions.csv", index=False)


if __name__ == "__main__":
    run()
