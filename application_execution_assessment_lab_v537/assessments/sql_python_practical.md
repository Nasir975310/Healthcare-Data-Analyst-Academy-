# Practical assessment — outpatient operations extract

**Timebox:** 90 minutes. Use `fixtures/clinic_ops.sqlite`. All records are synthetic.

## SQL tasks
1. Count source encounters and distinct encounter IDs.
2. Count completed, cancelled and no-show encounters.
3. Report completed encounter count and average wait by department.
4. Identify duplicated encounter IDs and their row counts.
5. Report completed encounter volume by calendar week.
6. List records with missing department, missing date or negative wait time.

## Python tasks
1. Load `encounters` from SQLite with pandas.
2. Report row count, duplicate encounter IDs, missing values and invalid wait values.
3. Create a cleaned analysis frame using documented rules; do not silently overwrite source rows.
4. Reconcile source rows, duplicate rows, excluded rows and retained rows.
5. Export a department summary CSV and a QA JSON file.

## Required memo
- State the grain and eligibility rules.
- Explain duplicate handling and why latest/valid record selection needs a documented rule.
- State the denominator for average wait.
- Identify at least two limitations.
- Do not infer clinical outcomes or causation from operations data.

## Scoring (100)
SQL 30; Python reproducibility 25; QA/reconciliation 20; interpretation 15; communication 10.
Integrity gate: no fabricated outputs, hidden exclusions or real patient data.
