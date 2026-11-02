# Professional Practicum — Release 3.3

Complete each project as if delivering to a real healthcare analytics client. The datasets are synthetic and designed to contain realistic quality and interpretation challenges.

## Suggested sequence
1. PRAC-01 Hospital performance review (5 working days).
2. PRAC-02 Antihypertensive DUE (5 working days).
3. PRAC-03 Remote client request-to-handoff (3 working days).

Do not start by opening the worked reference solution. First produce a scope note, data profile and analysis independently. Compare with solution guidance only after your first draft.

## Standard operating sequence
Request intake → clarification → metric contract → secure data handling → profiling → transformation → analysis → validation → interpretation → peer review → handoff → versioned archive.

## Dataset facts
- 600 synthetic encounters; patient IDs repeat across encounters.
- 1,600 medication order lines; 32 intentionally orphan encounter references.
- 120 service tickets; 8% approximately have no closed timestamp (exact count can be verified).
- Missing SBP and unit costs are intentional.
- Synthetic readmission flags are unvalidated.

## Run the supplied analysis
From Academy root:
```bash
python -m venv practicum/.venv
source practicum/.venv/bin/activate.fish  # Fish
# Bash/Zsh: source practicum/.venv/bin/activate
python -m pip install pandas numpy
python practicum/solutions/run_practicum_analysis.py
```
Outputs are written to `practicum/outputs/`. The script is a reference workflow, not a substitute for independent project work.

## Evidence required for portfolio
- Client brief and clarified requirements
- Data dictionary and metric contract
- Reproducible code / SQL / workbook
- Data-quality sign-off
- Analytical results and interpretation
- Limitations register
- Executive handoff
- README, environment and version history
- Reviewer feedback and changes

## Privacy and governance
Use synthetic data only. Never place patient identifiers, EHR exports, credentials, confidential client data or institutional extracts in a personal repo or unapproved AI/cloud service. Use an approved environment and written authorisation for real data.
