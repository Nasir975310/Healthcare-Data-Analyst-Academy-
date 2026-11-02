# End-to-end project workflow

1. Preserve `data/raw` as immutable source input.
2. Run `python run_project.py`.
3. Inspect `data/processed/quality_report.json` before interpreting results.
4. Review `data/quarantine/quarantined_encounters.csv`; understand why each record failed.
5. Confirm `accepted + quarantined = raw` and SQLite rows = accepted.
6. Open `data/processed/hospital_analytics.sqlite` in DBeaver and run `sql/analysis_queries.sql`.
7. Review the generated chart and report. Do not infer causality from descriptive summaries.
8. Run `python -m pytest -q`.
9. Complete `templates/case_study_template.md` with factual, reproducible findings.
10. Publish only synthetic data and scrub secrets, local paths and private notes.

## Windows and Linux
The project uses standard Python commands and runs from PowerShell, Bash or Fish after dependencies are installed. Activate the v4.7 virtual environment first, or create a new `.venv` in this project and install `requirements.txt`.
