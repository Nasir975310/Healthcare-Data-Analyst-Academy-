# v5.14.0 — Universal Statistical Analysis & Research Engine

A reproducible, CSV-driven Python analysis module with a browser-based educational planner.

## Quick start
From this directory:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
python scripts/analyze_study.py --input data/synthetic_bp_study.csv --outdir outputs
```
Outputs: `analysis_report.json`, `analysis_summary.csv`, and `analysis_report.html`.
Run tests: `python -m pytest -q tests`.

## Included
- Descriptive summaries, missingness, mean confidence intervals.
- Welch independent t-test, Mann–Whitney U, paired t-test, Shapiro–Wilk.
- Categorical cross-tabulation and Pearson chi-square with expected-count warning.
- Pearson/Spearman association and simple unadjusted linear regression.
- Mean-difference confidence interval, Cohen's d, source-file SHA-256 lineage.
- R reproducible source template and study analysis-plan guide.
- Browser planner for design/method selection and explanatory guardrails.

## Boundaries
The Python CLI performs calculations. The browser interface is a learning/planning surface and does not execute Python or R. The R script is a template and was not executed in this release QA. The example dataset is synthetic. No clinical inference, treatment recommendation, causal claim, sample-size calculation, missing-data imputation, or formal statistical analysis plan approval is provided. For real studies, prespecify the analysis and obtain qualified statistical/clinical review.
