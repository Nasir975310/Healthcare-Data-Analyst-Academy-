# v5.7.0 — Healthcare Analytics Data Engineering & ETL Orchestration

A local-first, reproducible CSV → validation → staging → curated SQLite pipeline with schema drift detection, incremental loading, rejected-row quarantine, run logs and reconciliation.

## Linux (Ryoku / Arch)
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/run_pipeline.py --input examples/encounters.csv --config config/pipeline.json --output-dir output
```

## Windows PowerShell
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py scripts\run_pipeline.py --input examples\encounters.csv --config config\pipeline.json --output-dir output
```

## Pipeline stages
1. Ingest CSV with a declared schema and source checksum.
2. Validate required fields, types, date format and value constraints.
3. Quarantine invalid records with row number and reasons.
4. Load accepted records into SQLite staging and curated tables.
5. Support incremental upsert by a configured primary key.
6. Detect missing/added/changed columns against the declared schema.
7. Produce run metadata, counts, logs, reconciliation and output hashes.

Run `python scripts/run_pipeline.py --help` for options. Use a fresh output directory for a clean run; SQLite history is retained if reusing the same output directory.

## Scheduling
Examples for Linux systemd user timers and Windows Task Scheduler are in `docs/scheduling.md`. Scheduling is not enabled automatically.

## Governance
The sample is synthetic. Do not process identifiable patient data without approved access, lawful basis, minimum-necessary controls, secure storage, retention policy and institutional approval. This pipeline is an educational ETL example, not a validated clinical system.
