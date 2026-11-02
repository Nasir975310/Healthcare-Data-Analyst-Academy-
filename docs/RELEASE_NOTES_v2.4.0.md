# Academy v2.4.0 — Healthcare Data Engineering and ETL Laboratory

## Added
- Dedicated Data Engineering view with eight progressive challenges.
- Local batch pipeline: CSV or paginated mock-API fixture extraction, raw payload storage, validation, normalisation, SQLite curated marts, quarantine, run logs, quality CSV and source SHA-256 manifest.
- Data contracts and pipeline architecture.
- Generic HTTPS REST extractor template with bearer-token environment variable, timeout, retry/backoff and full-next-URL pagination example.
- SQL audit queries for run history, mart grain, quality findings and encounter/order summaries.
- Linux systemd user timer and Windows Task Scheduler examples.
- Fish, Bash and PowerShell setup instructions.
- Included sample SQLite ETL database and sample run manifest/log/quality report.
- Local browser completion tracking for the ETL challenges.

## Tested behaviour
- CSV mode: 80 encounters and 150 medication orders ingested.
- Mock API mode: 80 encounters and 150 medication orders ingested after page-order and total-record checks.
- Injected orphan order: retained in raw layer, quarantined with reason, excluded from curated order mart (149 of 150 loaded).
- Repeated run: stable mart counts; separate run-log rows.
- Invalid zero quantity with `--fail-on-errors`: run stopped with nonzero exit code.
- Source files hashed into a JSON manifest.
- Optional unit-cost field correctly reported as not supplied by the base extract, not as 150 missing-cost errors.
- SQLite integrity check passed; SQL audit queries executed.

## Limitations
- Local educational batch pipeline, not production integration.
- Generic REST extractor is not connected to a real API and was not network-tested.
- No CDC, streaming, distributed orchestration, cloud deployment, alert delivery or PHI governance implementation.
- Scheduling files are examples and were not enabled on the user's machine.
- All data is synthetic.
