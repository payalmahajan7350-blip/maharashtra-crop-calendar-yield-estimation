# Interpretation scope

Final-model SHAP summaries are reported in the manuscript and supplement. This
code-and-calendar release does not include the processed predictor table,
frozen final-test predictions or serialized fitted estimators. If the required
processed table is obtained separately under applicable source-provider terms,
then after running the modeling script,
`python code/interpretability/recompute_shap.py` fits each
independently reproduced configuration on its refit partition and writes
`reproduced_results/optional_shap.csv`. It is an optional reanalysis and is not
the frozen manuscript SHAP table; package-version changes may alter its values.
Do not treat training Random Forest subset-selection ranks as final-model SHAP
or causal effects.
