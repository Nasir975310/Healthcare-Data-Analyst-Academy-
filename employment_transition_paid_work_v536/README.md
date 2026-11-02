# v5.36.0 — Employment Transition & Paid Work Launch

A practical bridge from training projects to truthful applications and carefully scoped first paid work. All case data in this module is fictional or synthetic.

## Start here
1. Complete `docs/evidence_to_claims.md` before editing a CV. Every technical claim must point to an artifact and a reproducible check.
2. Use `templates/healthcare_analyst_resume.md` and `templates/linkedin_github_profile.md`.
3. Attempt `assessments/take_home_challenge.md` under timed conditions, then score with `scripts/score_submission.py`.
4. Use `templates/freelance_statement_of_work.md` before agreeing to any client task.
5. Track activity in `templates/weekly_job_search_tracker.csv`.

## Run the assessment scorer
From this module directory:
```bash
python scripts/score_submission.py --input examples/sample_submission.json
python -m unittest discover -s tests -v
```
The scorer checks required evidence and basic SQL/Python answer properties. It is a coaching aid, not an employer decision or proof of competence.

## Scope and integrity
- State Pharm.D education accurately; do not imply prior analyst employment.
- Label the v5.32 practicum as synthetic and academic.
- Never upload patient-identifiable data, credentials, database dumps or employer-confidential material to a public repository or AI service.
- Do not claim Power BI Desktop, PostgreSQL deployment, GitHub publication or client delivery unless personally completed and evidenced.
- Freelance prices in the guide are illustrative planning scenarios, not market quotations or guaranteed earnings.
- For clinical analytics, define denominators, time windows, cohort rules and data provenance; do not make clinical decisions from a dashboard alone.
