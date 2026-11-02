# Healthcare Data Analyst Academy — v5.14.0

## Universal Statistical Analysis & Research Engine

This cumulative release adds an interactive analysis-planning view and a reproducible Python statistical workflow.

### New capabilities
- Descriptive statistics, distributions and missingness summaries.
- Welch independent t-test, paired t-test, Mann–Whitney U and Shapiro–Wilk checks.
- Categorical contingency tables with chi-square expected-count warnings.
- Pearson and Spearman association analyses.
- Simple unadjusted linear regression.
- Mean-difference confidence intervals and Cohen's d.
- Study-design-aware analysis planning for cohort, cross-sectional, RCT, case-control, paired and diagnostic-accuracy designs.
- Input SHA-256 provenance and JSON, CSV and HTML outputs.
- R source template and analysis-plan reference.

### Important boundaries
The browser module is an educational planner; it does not execute Python or R. The Python CLI is the calculation engine. The included dataset is synthetic and must not be interpreted as clinical evidence. The R template is included as source but was not executed during this release's QA.

### QA results
- 4 automated tests passed.
- Python CLI completed on the included 18-row synthetic dataset and produced JSON, CSV and HTML reports.
- 89 Python files compiled successfully.
- 221 JSON files parsed successfully.
- New JavaScript passed `node --check`.
- Full cumulative ZIP integrity checked after packaging.
