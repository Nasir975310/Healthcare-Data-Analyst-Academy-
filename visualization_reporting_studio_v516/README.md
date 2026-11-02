# v5.16.0 — Healthcare Data Visualization & Statistical Reporting Studio

## Quick start
```bash
python -m pip install -r requirements.txt
python scripts/visualize_study.py \
  --input data/synthetic_visualization_study.csv \
  --outdir outputs \
  --forest-csv data/synthetic_forest_effects.csv
python -m pytest -q tests
```
The script writes PNG figures, descriptive summaries, JSON diagnostics, Markdown and HTML reports.

## Included
- Histograms for numeric variables.
- Grouped box plot and descriptive summary table.
- Patient-level ROC curve and apparent AUC.
- Kaplan–Meier product-limit curves by group.
- Forest plot for supplied effect estimates and confidence intervals.
- SHA-256 source lineage and reproducible Python figure script.
- Interactive browser figure explorer with methodological interpretation prompts.

## Important limitations
- The browser view displays the generated example figures; it does not execute Python.
- ROC AUC is apparent performance on the supplied data, not validated predictive performance.
- Kaplan–Meier plots are descriptive only; no log-rank test, confidence bands, competing-risk model or Cox regression is calculated.
- Forest plots do not perform meta-analysis or pool estimates.
- All included data are synthetic. No real patient data are included.
