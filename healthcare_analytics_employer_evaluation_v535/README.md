# v5.35.0 — Portfolio Completion & Employer Evaluation

This release converts the synthetic hospital practicum into an employer-reviewable portfolio package and a scored job-readiness assessment. It includes a timed technical challenge, answer guidance, evidence-based rubric, portfolio hygiene audit, application tracker and interview bank.

## Run
From this directory:
```bash
python scripts/run_assessment.py
python scripts/portfolio_audit.py ../
python -m unittest discover -s tests -v
```
Run the v5.32 pipeline first if its SQLite warehouse is missing.

## Assessment rules
Suggested time: 120 minutes. Attempt the challenge before reading `assessments/ANSWER_KEY.md`. The automated assessment scores only machine-checkable items; the full rubric requires manual review.

## Integrity boundary
This is a self-directed educational project using synthetic data. Do not describe it as paid client work, employment, production hospital deployment or clinical evidence. Do not claim Power BI/PostgreSQL/GitHub execution without external evidence.
