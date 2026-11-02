# v5.45.0 — Portfolio Interview Readiness Lab

Turns the synthetic outpatient analytics project into a defensible interview demonstration. Includes a five-minute walkthrough, technical and stakeholder question bank, answer frameworks, a timed case exercise, a transparent self-assessment rubric, and a small scoring utility.

## Start here
1. Read `docs/INTERVIEW_WALKTHROUGH.md` and rehearse without reading the script.
2. Answer `docs/QUESTION_BANK.md` aloud; use the answer criteria, not memorized scripts.
3. Complete `docs/TIMED_CASE_EXERCISE.md` in 45 minutes using the portfolio's source files.
4. Score your evidence with `templates/SELF_ASSESSMENT.json`:

```bash
python -m portfolio_interview_readiness_v545.src.score_readiness   --input portfolio_interview_readiness_v545/templates/SELF_ASSESSMENT.json   --output portfolio_interview_readiness_v545/output/SELF_ASSESSMENT_REPORT.json
```

5. Run tests:

```bash
python -m unittest discover -s portfolio_interview_readiness_v545/tests -v
```

The score is a practice aid, not a validated hiring predictor. A high score does not establish employment readiness unless claims are backed by inspectable work. The project data are synthetic; never present them as real hospital data or claim clinical outcomes.
