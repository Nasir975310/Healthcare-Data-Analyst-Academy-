# v5.6.0 — Healthcare Analytics Data Governance & Quality Assurance Centre

Local-first controls for profiling datasets, running configurable validation rules, classifying issues, recording lineage and comparing dataset versions.

## Python validation

### Linux (Ryoku / Arch)
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/quality_audit.py --input ../report_generator_v54/data/report_sample.csv --output-dir output
```

### Windows PowerShell
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py scripts\quality_audit.py --input ..\report_generator_v54\data\report_sample.csv --output-dir output
```

Outputs: field profile, rule results, issue register, quality scorecard, lineage record and checksummed audit manifest. Rule configuration is explicit in `rules.json`; review thresholds for the project before operational use.

## Important
A quality score is a transparent rule-based indicator, not a certification. Rules cannot establish clinical validity or privacy compliance. Use minimum-necessary data, approved access, and synthetic/de-identified data for portfolio work.
