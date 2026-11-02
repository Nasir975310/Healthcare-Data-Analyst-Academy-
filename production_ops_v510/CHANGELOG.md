# v5.10.0 release notes

- Added an end-to-end CSV → validation/quarantine → SQLite curated warehouse → manifest/report pipeline.
- Added checksummed source lineage, schema version, UTC run timestamp, row counts and aggregate reconciliation metadata.
- Added repeatable upsert behaviour and database constraints/indexes.
- Added Linux systemd and Windows Task Scheduler templates, operations runbook and deployment checklist.
- Added tests for successful load and rejected-row quarantine.
- All data is synthetic. Scheduler templates were not installed or executed.
