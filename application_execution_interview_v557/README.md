# Application Execution & Interview Intelligence — v5.57

A local deterministic tool that turns a vacancy description and candidate profile into topic-specific interview questions, an evidence map, potential skill gaps and verification flags. It is not an AI model or hiring predictor.

## Run on Ryoku/Linux

```bash
cd application_execution_interview_v557
python -m unittest discover -s tests -v
python src/interview_pack.py examples/sample_vacancy.txt --profile examples/candidate_profile.json --title "Junior Clinical Data Analyst" --out output
```

Outputs: `output/interview_pack.md` and `output/interview_pack.json`.

For a real vacancy, save its complete description as UTF-8 text and edit the candidate profile. Remove skills you cannot demonstrate. Add only safe evidence references. Manually verify employer identity, vacancy, remote eligibility, location, shifts, salary and application channel.

**Integrity rules:** the Pharm.D thesis (prospective observational, N=153) is separate from synthetic portfolio projects. Label synthetic data clearly. Do not expose identifiable patient data. Verify all dates, skills, results and references before applications. Keyword detection can miss context; it does not prove competence or employer legitimacy.
