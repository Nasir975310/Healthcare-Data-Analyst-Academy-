# Reproduction and review protocol

## Environment
Python 3.10+; standard library only. No network access or third-party package required.

## Reproduce
From the project directory:
```bash
python src/run_project.py
python -m unittest discover -s tests -v
```
Outputs are generated under `outputs/`: JSON quality report, department CSV, SQLite database and SHA-256 manifest. The database is a generated artifact; do not commit it by default.

## Clean-room reproduction
1. Clone or copy the repository into a new directory.
2. Confirm the input CSV hash against the documented release manifest.
3. Run the two commands above.
4. Compare report counts and department summary with expected results.
5. Confirm the SQLite primary key constraint and query outputs.
6. Inspect `git status`; generated outputs and local databases should follow the ignore policy.

## Reviewer checklist
- Is the business question explicit?
- Are grain, cohort, exclusions and denominator documented?
- Can the reviewer reproduce every displayed number?
- Are duplicates, missingness and invalid values visible?
- Are source data, outputs and code versioned appropriately?
- Are limitations and synthetic-data provenance prominent?
- Are any patient identifiers, secrets, credentials or client materials present?
