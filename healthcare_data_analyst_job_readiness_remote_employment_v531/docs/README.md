# Job Readiness & Remote Employment Simulation v5.31

A practical employment-readiness module for entry-level healthcare analytics roles. All job postings and exercises are fictional training examples, not current vacancies.

## Run the readiness scorer
```bash
python scripts/score_readiness.py data/sample_candidate_scores.json
python -m unittest discover -s tests -v
```
Edit a copy of `data/sample_candidate_scores.json`; scores range 0–100 for each rubric domain. Output is written to `reports/readiness_result.json`.

## Use sequence
1. Read `job_descriptions/role_profiles.md` and choose two realistic role families.
2. Complete the timed questions in `assessments/technical_question_bank.md`.
3. Review your projects with `portfolio/portfolio_review_checklist.md`.
4. Practice `interviews/structured_interview.md`.
5. Score yourself using the rubric and scorer.
6. Build the 90-day plan from `docs/90_day_job_search_plan.md`.

## Score interpretation
- 85–100: strong portfolio readiness
- 70–84.99: developing job readiness
- 55–69.99: foundational; targeted practice required
- below 55: early-stage
A privacy/integrity breach blocks client-data readiness regardless of score. These are self-assessment bands, not employer certification or hiring predictions.

## Important
Never publish patient-identifiable data or use unapproved client data. Label academic and synthetic projects truthfully. A Pharm.D qualification is useful healthcare context but does not replace demonstrated analytics skills.
