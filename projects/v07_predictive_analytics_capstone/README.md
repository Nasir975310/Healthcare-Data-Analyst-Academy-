# V07 Predictive Analytics Capstone

**Educational synthetic-data project only. Not a clinical decision-support system.**

## What it does
- Generates a synthetic patient-level cohort with a binary 30-day readmission-like outcome.
- Validates identifiers, outcome domain and age range.
- Uses a stratified patient-level holdout split (one row per synthetic patient).
- Fits preprocessing inside scikit-learn pipelines.
- Compares logistic regression and random forest.
- Writes metrics, run metadata and validation notes.

The outcome is generated from an artificial formula. It does not represent real clinical risk, and model metrics must not be interpreted as evidence of clinical validity.

## Linux (Bash/Zsh)
From this directory:
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python scripts/run_capstone.py
```
For Fish:
```fish
python3 -m venv .venv
source .venv/bin/activate.fish
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python scripts/run_capstone.py
```
On Arch-based systems, use the distribution package manager for system tools; do not use `sudo pip` to modify system Python.

## Windows (PowerShell 7)
From this directory:
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
py scripts\run_capstone.py
```
If PowerShell blocks environment activation, do not weaken the machine-wide execution policy. You can run without activation:
```powershell
py -m pip --python .venv\Scripts\python.exe install -r requirements.txt
.\.venv\Scripts\python.exe scripts\run_capstone.py
```
If the `--python` pip option is unavailable in your pip version, invoke `.venv\Scripts\python.exe -m pip install -r requirements.txt`.

## Outputs
- `data/synthetic_patient_cohort.csv`
- `reports/model_metrics.csv`
- `reports/run_summary.json`
- `reports/validation.txt`

## Interpretation
Report AUROC and average precision alongside threshold-specific sensitivity, specificity, precision, confusion-matrix counts and Brier score. The 0.5 threshold is illustrative, not clinically selected. Calibration plots, confidence intervals, external validation, subgroup assessment and prospective evaluation are required before any real-world use.
