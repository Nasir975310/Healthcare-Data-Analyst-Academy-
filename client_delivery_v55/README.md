# v5.5.0 — Healthcare Analytics Client Delivery & Evidence Pack

This release adds a structured handoff workflow. It creates a client-facing delivery folder and ZIP from a project CSV plus optional report/dashboard artifacts, with source hashes, artifact inventory, metric contract, QA checklist, limitations and handoff notes.

## Generate a delivery pack

### Linux (Ryoku / Arch)
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/build_delivery_pack.py --project "Synthetic hospital operations" --input ../report_generator_v54/data/report_sample.csv --output-dir output
```

### Windows PowerShell
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py scripts\build_delivery_pack.py --project "Synthetic hospital operations" --input ..\report_generator_v54\data\report_sample.csv --output-dir output
```

Optional:
- `--report path/to/report.pdf`
- `--dashboard path/to/dashboard.html`
- `--data-dictionary path/to/data_dictionary.md`
- `--metric-contract path/to/metric_definitions.md`
- `--owner "Analyst or team"`
- `--period "Jan–Mar 2026"`

The tool copies supplied artifacts into a clean handoff folder, computes SHA-256 hashes, creates a manifest and a ZIP archive. It does not certify data quality or legal compliance.

## Handoff controls
Before delivery, confirm permissions, minimum necessary data, de-identification, recipient access, reporting grain, metric denominators, refresh date, limitations, and whether any small-cell or re-identification risk remains. Never deliver identifiable patient data in a public portfolio.
