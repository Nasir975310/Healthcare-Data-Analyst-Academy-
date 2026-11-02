# Release v5.32.0 — Healthcare Analytics Real-World Practicum

## Added
- Fictional hospital client brief and four synthetic source datasets.
- Python standard-library ETL and SQLite staging/curated warehouse.
- Data-quality profiling, source SHA-256 manifest and exception preservation.
- KPI summaries and monthly, encounter-type and medication-class extracts.
- SQL analysis queries, data dictionary, KPI dictionary and dashboard specification.
- Report template, client feedback simulation, change request log and handover checklist.
- Interactive graphical roadmap covering completed releases, pending deliverables and ten risk/solution pairs.
- Academy navigation entry and practicum view.

## QA
- 6 new practicum unit tests passed.
- Pipeline executed successfully.
- Source rows: 30 patients, 91 encounters, 170 observations, 129 medication orders.
- One orphan encounter (`E0091`) detected, preserved in staging and rejected from curated facts.
- SQLite integrity: `ok`; foreign-key violations: 0.
- v5.30 and v5.31 regression tests passed.
- Python compilation, roadmap JavaScript syntax and archive integrity checked.

## Limitations
- Entire dataset is synthetic.
- No live Power BI, PostgreSQL, EHR or client environment is deployed.
- Power BI dashboard specification requires implementation and runtime validation in Power BI Desktop.
- BP values are descriptive only; medication rows represent orders, not dispensing/adherence.
