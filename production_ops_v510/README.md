# v5.10.0 — Deployment, Automation & Production Operations

A standard-library Python + SQLite reference pipeline using synthetic encounter data. It validates an inbound CSV, quarantines invalid rows, incrementally upserts accepted records, and emits a run manifest and HTML quality report.

Run `python scripts/run_pipeline.py`. Review `output/run_manifest.json`, `output/quarantine.csv`, `output/quality_report.html`, and `output/curated_warehouse.sqlite`.

This is an educational reference implementation, not a production-ready clinical system. Scheduling templates are not installed. No real patient data, cloud deployment, alerting, secrets manager or external database is configured.
