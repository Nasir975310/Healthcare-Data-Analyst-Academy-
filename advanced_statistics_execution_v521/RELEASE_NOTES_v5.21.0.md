# Healthcare Data Analyst Academy v5.21.0

## Advanced Statistical Execution Environment

### Delivered
- pandas/NumPy descriptive profiling and variable-level missingness reports.
- Exploratory 1.5 × IQR outlier flags with flagged row indices (capped at 100 indices per variable).
- Independent two-group Welch t-test and Mann–Whitney U options.
- Welch confidence interval for the difference in means.
- Pearson chi-square with expected-cell diagnostics.
- Linear OLS and binary logistic regression with coefficient intervals and convergence status.
- Input SHA-256 provenance, runtime package versions, JSON results, CSV profiles and Markdown report.
- CSV, Excel and Parquet input support with appropriate optional dependencies.
- Synthetic dataset, JSON analysis configuration, dependency list and eight automated tests.
- Academy navigation and module guide.

### Limitations
- Complete-case regression; no imputation or missingness mechanism analysis.
- No automatic assumption checks, multiplicity correction, survival analysis, clustered/multilevel models, causal inference, propensity methods, or external validation.
- Chi-square expected counts are reported, but exact tests are not implemented.
- Mann–Whitney option also reports a Welch mean-difference CI; this interval is not a CI for a rank-based estimand.
- Logistic regression can fail or be unstable with separation, sparse data or convergence problems; convergence status is surfaced.
- Synthetic data is for software testing only, not clinical inference.
