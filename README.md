# Crop-calendar-aligned yield estimation: code and analytical calendar

Payal Mahajan and Madhav R. Fegade. This package accompanies the manuscript
"Machine Learning Framework for Retrospective District-Level Crop Yield
Estimation Using Weather and Satellite Data in Maharashtra, India".

## Scope

This is the author-approved **code-and-calendar release**, not a release of the
processed modelling dataset. It contains the study-defined analytical windows
for ten crop-season cases and scripts for calendar construction, cohort checks,
model fitting, metric verification and optional SHAP reanalysis. The calendar
dates are standardized analytical boundaries, not observed district/year-specific
sowing or harvest dates. The crop windows and five phases use half-open
membership `[start, end)` and unrounded equal elapsed-duration boundaries.

The scripts requiring `data/processed_modeling_data.csv`,
`data/frozen_test_predictions.csv` or `data/reported_crop_metrics.csv` cannot
reproduce the paper's numerical results from this archive alone. Those tables
are deliberately absent while redistribution conditions for source-derived APY
and FAO GAUL information are assessed. No raw APY, POWER, MODIS or GAUL files,
district geometry, frozen predictions or author-machine paths are included.
This archive should not be described as a complete one-command reproduction of
the published analysis.

## Crop-name mapping

The CSV retains the machine-readable crop keys used by the analysis. Their
manuscript labels (Table 7) are:

| CSV crop key | Manuscript label |
| --- | --- |
| Soyabean | Soybean |
| Cotton | Cotton |
| Sugarcane | Sugarcane |
| Rice | Rice |
| Tur | Tur |
| MaizeK | Kharif maize |
| GramR | Gram |
| WheatR | Wheat |
| JowarR | Jowar |
| MaizeR | Rabi maize |

The key spelling is preserved so that the calendar code matches archived
analysis files; this table changes no dates or boundaries.

## Contents

- `data/crop_calendar.csv`: ten analytical crop windows and provenance note.
- `code/feature_engineering/crop_calendar.py`: exact half-open phase construction.
- `tests/test_calendar.py`: calendar boundary smoke tests (no modelling data).
- `code/modeling/reproduce_models.py`: chronological selection/refit procedure;
  requires the non-redistributed processed modelling table.
- `code/preprocessing/validate_release.py`: cohort checks; requires that table.
- `code/evaluation/verify_frozen_metrics.py`: metric checks; requires frozen
  predictions and reported crop metrics, neither supplied here.
- `code/interpretability/recompute_shap.py`: optional post-hoc reanalysis;
  requires the processed table and installed modelling dependencies.

## Running the calendar check

Use a Python environment with the packages named in `requirements.txt`. From
the archive root, run:

```text
python -m unittest discover -s tests -v
```

The modelling scripts resolve input paths relative to this archive. Providing
the withheld tables privately, if permitted, is a separate step. The original
environment lockfile is unavailable, so library/runtime differences may cause
small refit variation; a successful calendar test does not verify the frozen
paper metrics.

## Reuse and source data

Author-owned code in `code/` and `tests/` is licensed under MIT (see
`LICENSE_CODE.txt`). The author-defined calendar in `data/crop_calendar.csv` is
licensed under Creative Commons Attribution 4.0 International (see
`LICENSE_CALENDAR.md`). These grants do not apply to third-party source data.

For source provenance and access, see the manuscript's Data Sources section.
NASA POWER's [referencing guide](https://power.larc.nasa.gov/docs/referencing/)
asks users to cite the service/version/access date and requests notification
when data are transmitted to other researchers. The [MOD13Q1 catalog](https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MOD13Q1)
and [MOD11A2 catalog](https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MOD11A2)
state that LP DAAC MODIS products have no subsequent use or redistribution
restrictions. The [APY provider policy](https://desagri.gov.in/website-policies/)
requires permission and acknowledgement for reproduction, and the
[FAO GAUL 2015 licence](https://developers.google.com/earth-engine/datasets/catalog/DataLicenseGAUL2015.pdf)
contains derivative-data and redistribution conditions. These terms must be
checked before any source-derived analytical table is released. No DOI is
claimed in this local package; cite the verified archive DOI after deposit.
