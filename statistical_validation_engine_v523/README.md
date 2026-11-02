# Statistical Validation Engine v5.23.0

Extends v5.21 statistical execution with assumption diagnostics, bootstrap confidence intervals, regression diagnostics and multiple-testing correction.

## Run

From the Academy root:

```bash
python -m pip install -r statistical_validation_engine_v523/requirements.txt
python statistical_validation_engine_v523/scripts/validation_engine.py \
  --input advanced_statistics_execution_v521/data/synthetic_healthcare_dataset.csv \
  --config statistical_validation_engine_v523/templates/validation_config.json \
  --output statistical_validation_engine_v523/outputs/demo
```

## Capabilities
- Shapiro–Wilk normality diagnostics per independent group.
- Median-centred Levene variance-homogeneity test.
- Linear OLS diagnostics: Breusch–Pagan, residual normality, HC3 robust SE/CI, Cook's distance, leverage, VIF and condition number.
- Binary logistic model convergence and coefficient/odds-ratio reporting.
- Reproducible percentile bootstrap mean intervals with fixed seed.
- Holm, Benjamini–Hochberg (FDR) and Bonferroni p-value adjustment.
- JSON, Markdown and SHA-256 manifest outputs.

## Important
This is a diagnostics and validation layer, not an automatic test selector. Diagnostics do not prove assumptions. Bootstrap requires an independent-observation sampling design. Logistic regression can be unstable or fail with separation/sparse data; no Firth correction is provided. No imputation, clustered bootstrap, multilevel model, survival analysis, causal inference, external validation or clinical decision support is included. Use only governed data; never put identifiable patient records in portfolio materials.
