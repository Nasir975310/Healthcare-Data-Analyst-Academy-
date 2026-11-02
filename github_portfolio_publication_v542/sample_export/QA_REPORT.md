# v5.38.0 QA report

- New module unit tests: 5/5 passed.
- End-to-end project run: passed using Python standard library.
- Reconciliation: 24 raw rows → 1 duplicate removed → 23 deduplicated rows.
- Eligible completed encounters: 20; valid nonnegative wait denominator: 18.
- Department summary: Cardiology 7 / mean 21.29 min; General Medicine 7 / mean 32.60 min (n=5); Orthopaedics 6 / mean 33.67 min.
- Output generation: JSON quality report, department summary CSV, SQLite database and SHA-256 manifest passed.
- SQLite deduplicated row count: 23; encounter_id primary key enforced.
- Repository preflight: 0 findings on this module; separate dummy-secret test correctly detected a deliberately constructed test token.
- Python syntax compilation and roadmap JavaScript syntax: passed.
- Academy HTML static parse: no duplicate IDs; v5.38 roadmap navigation link present.
- External deployment, public GitHub publication and client review: not performed.

The Python runtime emitted a spreadsheet warmup warning at startup; it did not prevent the project tests or pipeline from passing. The repository preflight is heuristic and is not a security certification.
