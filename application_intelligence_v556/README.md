# v5.56.0 — Application Intelligence & Job Search Execution

A local, explainable job-description evaluator for entry-level healthcare analytics and adjacent Pharm.D roles. Standard-library Python; no network access, account connection, API key or AI claim.

## Run on Ryoku / Linux

```bash
cd application_intelligence_v556
python src/jobfit.py examples/sample_job_description.txt --profile examples/sample_profile.json --out output
```

Replace the example job description with a UTF-8 `.txt` file. Edit the profile JSON first: remove any skill you cannot demonstrate and do not overstate experience. Outputs are `assessment.md` and `assessment.json`.

## Included
- Role-family detection across healthcare analytics, clinical data, research coordination, pharmacovigilance, MIS/reporting and RWE.
- Explainable dimension scores, detected skills, experience and education barriers.
- Textual risk prompts for fees, sensitive credential requests, unrealistic pay and vague contact channels.
- Human review checklist, scoring methodology and seven automated tests.

## Interpretation
The score is a prioritisation aid, not an ATS score or hiring probability. It does not verify employer legitimacy, remote status, vacancy availability, salary or credentials. Keyword matching is imperfect. Always inspect the full job description and verify the employer independently.

## QA
Run `python -m unittest discover -s tests -v`. The example vacancy is fictional and illustrative. No live vacancies were searched and no applications were submitted.
