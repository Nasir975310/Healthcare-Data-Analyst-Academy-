# Vacancy Sourcing & Evidence Capture — v5.60

A local workflow for collecting vacancy records from sources you independently visit, preserving user-supplied excerpts with hashes, detecting duplicate candidates and prioritising a shortlist against an editable profile.

**It does not search the web, scrape job boards, verify employers or submit applications.** The included vacancies are fictional training examples.

## 1. Capture source evidence

Save the relevant vacancy text to a UTF-8 file, then run:

```bash
python -B src/capture_evidence.py \
  --vacancy-id S-101 \
  --source-url 'https://example.com/careers/role' \
  --source-name 'Employer careers page' \
  --excerpt-file vacancy_excerpt.txt \
  --out evidence
```

This creates a text snapshot and JSON manifest with UTC capture time and SHA-256. A hash protects against unnoticed file changes after capture; it does not prove the source is genuine or that the vacancy remains open.

## 2. Maintain the registry

Copy `templates/vacancy_source_registry.csv` to a private working directory. Add one row per source listing. Record exact source URL, independently located employer URL, capture time, date found, deadline, location, remote conditions, required skills, eligibility notes, evidence filename/hash and status.

## 3. Prioritise the shortlist

Edit `examples/candidate_profile.json` to accurately reflect your skills, domain experience and years of work experience. Do not count academic or synthetic projects as paid employment.

```bash
python -B -m unittest discover -s tests -v
python -B src/vacancy_shortlist.py \
  examples/demo_registry.csv \
  --profile examples/candidate_profile.json \
  --as-of 2026-11-02 \
  --out shortlist_output
```

Open `shortlist_output/shortlist.html`; inspect the full `shortlist.json` for the detailed skill and experience comparison.

## Score interpretation

The priority score is a transparent heuristic built from detected profile-skill matches, healthcare-domain match, experience fit and listed required-skill matches. It is not an ATS score, a qualification decision or a probability of getting hired. Manually inspect mandatory criteria, work authorisation, location, shifts, salary, degree eligibility and employer legitimacy.

## Privacy and provenance

Keep private tracker data outside public repositories. Do not store Aadhaar/passport numbers, bank details, passwords, OTPs, patient information or confidential recruiter messages. Never mark a vacancy verified based only on a search snippet or the presence of HTTPS.
