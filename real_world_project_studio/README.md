# Real-World Healthcare Analytics Project Studio (v3.9)

All records are fabricated and deterministic. They are not real patients, real hospital operations, real adverse-event reports, or evidence of drug effectiveness.

## Projects
1. **Hospital operations performance pack** — encounter grain, operational KPIs, source quality, safe joins and management narrative.
2. **Antihypertensive drug-utilisation evaluation** — cohort description, paired BP summaries, prescribing patterns and non-causal interpretation.
3. **Pharmacovigilance case-quality review** — case workflow, duplicate candidates, chronology, seriousness and data-quality reporting.

## Reproduce
Python 3.10+ recommended. From this directory:
```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python scripts/run_all.py
```
Outputs are written to `outputs/`. The scripts use pandas and standard-library modules. They do not connect to any EHR, hospital, regulator, or live API.

## Data governance
Do not replace synthetic data with patient-level data unless you have explicit institutional authorization, an approved secure environment, minimum-necessary access, and applicable ethics/privacy approvals. Never commit PHI, credentials, or identifiable records to GitHub. Small-cell suppression and disclosure review are context-dependent and must be agreed with the data owner.

## Important interpretation boundaries
- Encounter rows are encounter-level, not unique-patient rows.
- `readmission_flag` is a supplied synthetic field; it is not validated against a time-window definition or linked subsequent encounter logic.
- A prescription/order does not prove dispensing, administration, ingestion, persistence, or adherence.
- The DUE dataset is synthetic observational data. Pre/post differences and between-group differences do not establish treatment causality.
- Pharmacovigilance flags are training labels. Duplicate candidates are not confirmed duplicates; seriousness is not severity; no signal or causality conclusion is generated.
