# v5.7.0 — Healthcare Analytics Data Engineering & ETL Orchestration

- Added a browser-local ETL validation preview with configurable required fields, primary key, date and numeric rules, quarantine export and reconciliation.
- Added Python CSV-to-SQLite pipeline with schema drift detection, validation, row-level quarantine, staging history, curated incremental upsert and run metadata.
- Added source/config/output SHA-256 manifest, run summaries and pipeline logs.
- Added SQL analytics examples, Linux systemd user timer and Windows Task Scheduler guidance.
- Synthetic fixture intentionally includes duplicate/blank keys, invalid date, negative numeric values and out-of-range/missing SBP.
- SQLite load and SQL queries executed successfully in QA. Scheduling examples are documentation only and were not activated.
