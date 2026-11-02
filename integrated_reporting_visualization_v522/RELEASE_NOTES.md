# Healthcare Data Analyst Academy v5.22.0

## Release focus
Integrated reporting and visualization: connect tabular descriptive outputs, figures, reports and provenance into one reproducible local workflow.

## Included
- Configuration-driven Table 1 (continuous mean ± SD; categorical n (%), optional group stratification).
- Histograms and grouped boxplots.
- Display-only forest plots and regression coefficient plots using supplied estimates and intervals.
- Apparent ROC curve and descriptive Kaplan–Meier curve.
- Executive and technical Markdown reports.
- Input/output SHA-256 evidence manifest and output validation.
- Explicit, non-destructive export to the v5.17 publication workbench.

## QA performed
- v5.22 automated tests: 6 passed.
- Synthetic end-to-end demo: 20 rows, 8 figures, output validation passed.
- v5.22 to v5.17 handoff: completed; 13 files copied and hashed.
- Regression suites: v5.19 (7), v5.18 (5), v5.17 (5), v5.15 (5) passed. v5.21, v5.20 and v5.16 regression suites were not counted as passed because they exceeded the available per-suite execution window.
- Repository syntax/asset checks are recorded in the release summary supplied with this package.

## Important limits
ROC is apparent only and is not validation. Kaplan–Meier excludes confidence intervals, log-rank testing, Cox regression and competing-risk methods. Forest plots do not pool estimates; coefficient plots do not fit models. Table 1 is descriptive and does not establish group equivalence. No automatic assumption checking, imputation, multiplicity correction or causal inference is provided. Synthetic data only in the included demo.
