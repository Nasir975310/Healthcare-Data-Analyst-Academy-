# v5.21.0 — Advanced Statistical Execution Environment

A reproducible local analysis engine using pandas, NumPy, SciPy and statsmodels. It generates a JSON result manifest, descriptive and missingness CSVs, and a Markdown report.

## Install dependencies

```bash
python -m pip install -r requirements.txt
```

## Run the synthetic example

```bash
python scripts/statistical_engine.py \\
  --input data/synthetic_healthcare_dataset.csv \\
  --config templates/analysis_config.json \\
  --output outputs/demo_analysis
```

Supported input: CSV, XLSX/XLS (requires openpyxl), and Parquet (requires pyarrow). Configure optional sections in JSON: `outlier_columns`, `group_comparison`, `categorical_test`, and `regression`.

### Methods
- Descriptive profile: n, missingness, unique values, mean/SD, median/IQR and range for numeric variables; mode for nonnumeric variables.
- Missingness report by variable.
- Exploratory outlier flags using 1.5 × IQR fences. Flags are not deletion instructions.
- Two independent-group comparisons: Welch t-test or Mann–Whitney U. The reported confidence interval is a Welch mean-difference interval even when Mann–Whitney is selected; do not interpret it as a CI for the rank-based estimand.
- Pearson chi-square test with expected-cell diagnostics.
- Linear OLS or binary logistic regression with coefficient confidence intervals.

## Statistical and clinical limitations
The engine does not automatically select tests, verify study design, diagnose assumptions, adjust for multiple comparisons, impute missing values, perform propensity methods, survival analysis, clustered/multilevel modelling, robust variance estimation, or external validation. Logistic regression may fail or be unstable with separation or sparse data. The small synthetic example is for software testing, not clinical inference. Interpret results with the protocol, data dictionary and a qualified reviewer.
