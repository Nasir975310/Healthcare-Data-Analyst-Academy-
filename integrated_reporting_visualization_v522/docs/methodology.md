# v5.22 reporting methodology

- Table 1: continuous variables are reported as mean ± sample SD; categorical variables as n (%). Group-stratified rows are descriptive. No inferential p-values are automatically inserted.
- Forest plot: displays supplied ratio-scale estimates and confidence intervals. The pipeline does not pool studies or calculate a meta-analysis.
- Regression coefficient plot: displays supplied model-scale coefficients and confidence intervals; interpretation depends on the originating model and coding.
- ROC: apparent/resubstitution ROC only. The same sample is used for score evaluation; no split-sample, bootstrap, cross-validation, calibration or external validation is performed.
- Kaplan–Meier: descriptive product-limit estimate with right-censoring. No confidence intervals, log-rank test, Cox model or competing-risk method is included.
- Figures are rendered at 300 dpi. Output manifest records file sizes and SHA-256 hashes.
- These are educational tools, not validated clinical decision support. Synthetic demo data are not patient observations.
