# Healthcare Data Analyst Academy — v5.16.0

## Healthcare Data Visualization & Statistical Reporting Studio

### New capabilities
- Python figure-generation pipeline using pandas, NumPy and Matplotlib.
- Histograms for numeric variables and grouped box plot with descriptive summary CSV.
- Patient-level ROC curve with apparent AUC and JSON summary.
- Kaplan–Meier product-limit curves by group with JSON curve summaries.
- Forest plot for supplied positive ratio estimates and confidence intervals on a log scale.
- HTML and Markdown reports, PNG figures and SHA-256 input lineage.
- Interactive Academy gallery with category filtering and publication-quality interpretation guidance.

### QA results
- v5.16 automated tests: 5 passed.
- v5.15 regression tests: 5 passed.
- v5.13 regression tests: 3 passed.
- v5.14 regression tests: 4 passed.
- 93 Python files compiled.
- 226 JSON files parsed.
- New JavaScript passed `node --check`.
- Eight image references in the Academy view resolve to generated figure files.
- HTML IDs checked for duplicates; none found.
- End-to-end figure/report generation completed using a 20-row synthetic dataset.
- ZIP integrity checked after packaging.

### Scope boundaries
- ROC AUC is apparent performance on the supplied data and is not validation.
- Kaplan–Meier is descriptive only; no log-rank test, confidence bands, competing-risk model or Cox model is included.
- Forest plot displays supplied estimates; no pooled meta-analysis or heterogeneity calculation is included.
- Browser gallery displays generated files; it does not execute Python.
- All example data are synthetic.
