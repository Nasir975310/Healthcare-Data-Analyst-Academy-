# Job Search Source & Vacancy Verification — v5.59

Offline vacancy register, URL-based duplicate detection, deadline checks and a structured human verification checklist. It does not browse the internet or certify employers.

## Run on Ryoku / Linux

```bash
cd job_search_source_vacancy_verification_v559
python -m unittest discover -s tests -v
python src/vacancy_registry.py examples/demo_registry.csv --as-of 2026-11-02 --out demo_output
```

Open `demo_output/vacancy_report.html`. The included example employers and vacancy records are fictional.

## Use with real vacancies

1. Copy `templates/vacancy_registry.csv` into a private folder.
2. Create one unique `vacancy_id` per vacancy.
3. Record the exact source URL and an employer URL found independently (not merely copied from an unsolicited message).
4. Set each verification field to `yes`, `no`, `unknown` or `not_applicable`.
5. Run with the current review date: `--as-of YYYY-MM-DD`.
6. Investigate warnings manually using the employer's independently located official careers page and contact details.

## What the checks mean

- `employer_domain_checked`: you inspected the domain and checked for impersonation/misspellings.
- `vacancy_on_official_site`: you independently located the same vacancy on the employer's official careers site or obtained confirmation from an independently verified contact.
- `recruiter_identity_checked`: recruiter identity and authority were checked through an independent channel.
- `no_upfront_fee_confirmed`: no payment is required for application, interview, equipment or placement.
- `privacy_request_checked`: the process does not request OTPs, passwords, bank credentials or unnecessary identity documents.

A row can be marked eligible for human final review only when all five checks are `yes`, a separate employer URL is recorded and the deadline has not passed. This is a workflow gate, not proof of legitimacy or a guarantee of safety.

## Duplicate detection

Normalises host casing, default ports, repeated/trailing slashes, tracking parameters and query ordering. It cannot detect the same vacancy posted at different URLs or mirrored by different domains. Review suggested duplicates manually.

## Privacy

Do not store Aadhaar/passport numbers, bank information, OTPs, passwords, patient information or confidential recruiter communications in the registry. Keep real application data out of public Git repositories.
