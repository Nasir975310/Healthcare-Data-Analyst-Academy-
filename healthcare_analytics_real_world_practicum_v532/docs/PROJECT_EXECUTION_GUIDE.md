# Project execution guide

## 1. Start with the client brief
Read `docs/CLIENT_BRIEF.md`, identify the six business questions and confirm exclusions.

## 2. Inspect raw inputs
Files are in `data/raw/`. Review `DATA_DICTIONARY.md` and verify each file's row count, key and grain.

## 3. Execute the pipeline
```bash
python src/run_project.py
```
The pipeline writes a SQLite database and JSON/CSV outputs to `deliverables/`. It creates staging and curated tables, preserves the orphan encounter in staging and excludes it from the curated encounter fact.

## 4. Review outputs
- `data_quality_report.json`
- `kpi_summary.json`
- `monthly_encounters.csv`
- `medication_class_utilization.csv`
- `encounters_by_type.csv`
- `source_manifest.json`

## 5. Complete the client-facing work
Use the report template, KPI dictionary, dashboard spec and simulated change requests. Build the Power BI report only in a supported runtime and record actual validation evidence.

## 6. Complete tests
```bash
python -m unittest discover -s tests -v
```

## 7. Final handover
Complete `DELIVERY_CHECKLIST.md`. Do not mark acceptance until each client change request is implemented and retested.
