# Contributing

Improve learning clarity, correctness, reproducibility, accessibility or maintainability.

## Before changing files
1. Read `SECURITY.md`, `DATA_HANDLING_POLICY.md` and `LICENSE_DECISION_REQUIRED.md`.
2. Check the module's prerequisites in `MODULE_COMPATIBILITY_MATRIX.md`.
3. Keep changes scoped; avoid unrelated module rewrites.
4. Use synthetic fixtures. Never commit PHI, patient identifiers, credentials, tokens or confidential institutional material.
5. Add/update tests, expected outputs and module documentation.

## Local checks
```bash
python -m pip install pytest
python -B -m pytest -q
python -B scripts/verify_release.py
python -B scripts/validate_release_docs.py
python -B scripts/verify_local_links.py
```

Run the historical isolated audit separately when dependencies and time allow:
```bash
python -B scripts/verify_full_academy.py --timeout 30 --jobs 1 --output FULL_TEST_REPORT.json
```

A passing root suite does not certify every course-pack.

## Pull request checklist
- [ ] Scope and intended learner outcome are clear.
- [ ] Data source, grain and assumptions are documented.
- [ ] Metric definitions specify numerator, denominator, exclusions and time window.
- [ ] Tests or manual verification steps are included.
- [ ] No real patient or confidential data is included.
- [ ] Dependencies and setup instructions are updated.
- [ ] Limitations and known failures are disclosed.
