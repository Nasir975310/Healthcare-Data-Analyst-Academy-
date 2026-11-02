# Synthetic Outpatient Operations Analytics

A reproducible Python/SQLite portfolio project using a small synthetic outpatient encounter dataset.

## Question
How can encounter-level records be validated and summarized into transparent outpatient volume and wait-time measures?

## Run
Python 3.10+ is recommended. No third-party Python packages are required.

```bash
python src/run_project.py
python -m unittest discover -s tests -v
python scripts/repository_preflight.py
```

The pipeline writes quality JSON, department summary CSV, SQLite database and a SHA-256 manifest under `outputs/`. Generated runtime files should not be committed.

## Reference results
See `CASE_STUDY.md` and `docs/reference_results.md`. The dataset is synthetic; results do not describe a real hospital.

## Data and metric rules
See `docs/data_dictionary.md` and `docs/metric_contract.md`. Encounter grain, deduplication policy, eligibility criteria, valid wait-time denominator and exclusions are documented.

## Limitations
This is an educational demonstration, not clinical decision support, a validated hospital performance study, or evidence of paid professional experience. It does not establish causal relationships or clinical outcomes.

## Privacy and provenance
The included fixture is synthetic. Do not add real patient data, personal information, credentials, tokens or confidential employer data.

## License
No license is assigned by this generated export. Choose and add a license only after confirming you have the right to license all included material.
