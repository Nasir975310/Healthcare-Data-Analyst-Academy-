# Production operations runbook

## Pipeline contract
Input: UTF-8 CSV with required columns defined in `config/pipeline.json`. Output: curated SQLite warehouse, row-level quarantine CSV, JSON run manifest and HTML quality report. The sample is synthetic.

## Run locally
From this module directory:
- Linux/Ryoku: `python scripts/run_pipeline.py`
- Windows PowerShell: `py scripts/run_pipeline.py`
- Custom paths: `python scripts/run_pipeline.py --input /path/to/file.csv --output-dir /path/to/output`

Exit code 0 means the run completed. `PASS_WITH_QUARANTINE` means processing completed but rejected rows require review. A successful process exit is not a clinical or business data-quality certification.

## Operational controls
1. Stage immutable source files; never overwrite the only raw copy.
2. Record source checksum, schema version, run timestamp and counts.
3. Inspect quarantine and reconcile rows read = accepted + rejected.
4. Reconcile curated row counts and aggregate totals against source SQL.
5. Monitor disk space, job duration, failure rate and stale-data age.
6. Restrict output and logs; do not log direct identifiers or sensitive clinical fields.
7. Use least-privilege service accounts and encrypted storage/backups.
8. Define retention, recovery point objective and recovery time objective before production.
9. Promote changes through development → test → production with versioned configuration and rollback.
10. Never run this teaching fixture against real patient data without privacy, security, governance and clinical validation.

## Scheduling
Examples in `scheduling_examples.md` are templates only; they were not installed or scheduled by this release. Add alerting and an operator-owned failure escalation path before production use.
