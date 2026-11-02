# Platform and scheduling guide — ETL v2.4.0

## CachyOS / Ryoku / Fish
From the Academy root:
```fish
python -m venv .venv
source .venv/bin/activate.fish
python -m pip install -r requirements-etl.txt
python scripts/healthcare_etl_pipeline.py --source csv
python scripts/healthcare_etl_pipeline.py --source mock-api
```
If Fish activation is unavailable, call the environment interpreter directly:
```fish
.venv/bin/python scripts/healthcare_etl_pipeline.py --source csv
```
Open the SQLite database in DBeaver:
`assignments/outputs/healthcare_etl_training.db`

## Linux scheduling
See `etl/systemd/README.md`. First run the pipeline manually. Then install the user timer and inspect logs with `journalctl --user`.

## Windows PowerShell
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements-etl.txt
py scripts\healthcare_etl_pipeline.py --source csv
```
For Task Scheduler, see `etl/windows/README.md`.

## Generic API extractor
`scripts/healthcare_api_extractor_template.py` is a template, not a live integration. It expects an HTTPS endpoint that returns:
```json
{"results":[{"id":"synthetic-example"}],"next":null}
```
Configure `HDA_API_BASE_URL`, `HDA_API_ENDPOINT`, and `HDA_API_TOKEN` as environment variables. Never commit tokens or paste credentials into the Academy. Confirm authentication, pagination, rate limits, allowed data scope, retention and audit requirements with the API owner before connecting any real system.

## What is and is not implemented
- Implemented: local CSV ingestion, local paginated JSON fixture ingestion, raw payload storage, validation, normalisation, orphan quarantine, SQLite upsert, run log, quality report, file checksums and manifest.
- Not implemented: real API integration in the Academy run path, CDC, streaming, distributed orchestration, automated alert delivery, cloud deployment, PHI governance or high availability.
- Repeated identical runs are tested for stable key counts. Full incremental CDC and late-arriving correction handling are not implemented.
