# Local reproduction protocol

Run from the extracted Academy root. Commands below assume Linux/macOS and Python 3.10+.

```bash
cd portfolio_execution_reproducibility_v538
python --version
python src/run_project.py
python -m unittest discover -s tests -v
python scripts/repository_preflight.py
```

Record the actual output and exit codes. The pipeline writes `outputs/quality_report.json`, `outputs/department_summary.csv`, `outputs/analytics.sqlite` and `outputs/sha256_manifest.json`. The SQLite file is a runtime artifact and should not be committed unless there is a deliberate reason.

Compare the generated quality report and department CSV with the v5.40 reference artifacts. Differences may result from changed source files or code; investigate rather than overwrite expected values blindly.

For a clean-copy check, extract the archive to a new directory and repeat the commands. A run from the original working directory is not a clean-copy reproduction.

## Required evidence
- OS/version and Python version
- Exact commands
- Exit code for each command
- Captured stdout/stderr
- SHA-256 of source CSV and generated outputs
- Any differences and their explanation
- Confirmation that no real patient data or credentials were introduced
