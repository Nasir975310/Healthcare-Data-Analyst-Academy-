# v5.13.0 — Universal Data Dictionary & Study Validation Engine

This module adds:
- reusable starter variable dictionary;
- configurable required, unique, numeric range, category, date, temporal and cross-field rules;
- executable Python CSV validator;
- JSON, CSV issue and HTML quality reports;
- source SHA-256 lineage and completeness summary;
- synthetic fixtures and automated tests;
- validation methodology and dictionary governance guidance.

Run:
`python scripts/validate_dataset.py`

Custom input:
`python scripts/validate_dataset.py --input path/to/data.csv --output-dir output`

Exit code 0 = no configured errors; exit code 1 = configured errors found. Warnings can still exist. This is deterministic data-quality screening, not clinical validation or statistical analysis.
