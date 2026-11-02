# Healthcare Data Analyst Academy v5.24.0

## Clinical Research Methods & Advanced Modelling
- Mann–Whitney U with Cliff's delta and bootstrap CI.
- Paired Wilcoxon signed-rank plus a separately labelled bootstrap interval for mean change.
- Friedman repeated-measures test and Kendall's W.
- Repeated stratified K-fold logistic prediction with out-of-fold ROC AUC, Brier score and calibration intercept/slope.
- Independent two-sample mean power/sample-size planning.
- Descriptive missingness pattern summaries.
- Machine-readable results, Markdown report and SHA-256 evidence manifest.

## QA
- v5.24: 9 tests passed.
- Regression: v5.23 (8), v5.22 (6), v5.21 (8), and combined v5.19/v5.18/v5.17/v5.15 (22) passed.
- Total: 53 tests passed.
- Synthetic end-to-end demo: 120 rows; all six configured analysis categories executed.
- Repository: 111 Python files compiled, 257 JSON files parsed, 55 JavaScript files syntax-checked; zero errors, duplicate HTML IDs or missing script assets.

## Limits
No multiple imputation, nested CV, external validation, post-hoc Friedman contrasts, clustered bootstrap or design-specific power procedures. Internal validation is not external validation. Missingness summaries do not identify MCAR/MAR/MNAR. Included demo is synthetic.
