# Getting started

## Choose one route
Use [LEARNING_PATHS.md](LEARNING_PATHS.md) to select a beginner, SQL/BI or Python/data-engineering route. Each phase should end with an inspectable output: workbook, query pack, validated dataset, notebook, dashboard specification or case study.

## Open the academy
Open `index.html` in Firefox or Chromium. It is a local static entry point.

## Suggested core tools
- Excel or LibreOffice Calc for spreadsheet work.
- SQLite or PostgreSQL plus DBeaver for SQL.
- Python 3.10+ with pandas, NumPy, Matplotlib and Jupyter for analysis.
- Git for version control.
- Power BI Desktop on a supported Windows environment, or a documented Linux alternative.

Install only dependencies needed for the module being studied. See `MODULE_COMPATIBILITY_MATRIX.md`.

## Repeatable project workflow
1. Define the analytical question and intended audience.
2. Inspect the data dictionary, grain, time coverage and missingness.
3. Validate row counts, duplicates, joins and allowed values.
4. Define metrics before querying or visualising.
5. Produce SQL/Python analysis with reproducible inputs.
6. Reconcile key outputs independently.
7. Explain findings, uncertainty and limitations.
8. Save tests, environment details and a portfolio-safe summary.

Update `PROGRESS_TRACKER.md` with actual evidence. A plan is not a completed output, and a local pass is not a remote CI pass.

## Data safety
Use synthetic or explicitly approved de-identified datasets. Never commit PHI, patient identifiers, credentials, API keys or institution-confidential data. Educational analytics are not clinical decision support and must not direct patient care.
