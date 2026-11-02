# Release v5.30.0 — Healthcare Analytics Capstone & Employment Assessment

## Added
- Synthetic hospital client brief with four source CSV tables.
- Python standard-library profiling, staging, curated SQLite warehouse and KPI pipeline.
- SQL analysis query set, KPI dictionary and dashboard specification.
- Employer-style 100-point assessment rubric and client handover checklist.
- Integrated Academy navigation entry and capstone view.

## QA
- 5 unit tests passed.
- Pipeline executed successfully.
- SQLite integrity check: `ok`; foreign-key violations: 0.
- One intentionally orphaned encounter detected in source staging and rejected from curated encounter fact.
- All data are synthetic.

## Limitations
- This is a training capstone, not a production clinical system.
- BP metrics are descriptive only.
- No live Power BI deployment, external database, or clinical terminology validation is included.
