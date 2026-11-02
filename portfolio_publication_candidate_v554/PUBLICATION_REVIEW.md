# Public repository release review

This checklist is intentionally incomplete until a human reviews the exact repository contents and selects a license.

## Data and provenance
- [ ] Confirm every row in `data/synthetic_outpatient_encounters.csv` is generated synthetic data.
- [ ] Confirm no real patient, employee, institution, or client information is present.
- [ ] Confirm no confidential material or third-party proprietary data is included.
- [ ] Review the full commit diff and every file, not only scanner output.

## Security and repository hygiene
- [ ] Confirm no tokens, passwords, private keys, personal paths, or private URLs are present.
- [ ] Confirm generated runtime databases, logs, caches and virtual environments are excluded.
- [ ] Run `python scripts/repository_preflight.py`.
- [ ] Inspect `.gitignore` and the final staged file list.

## Licensing
- [ ] Choose an appropriate license after checking ownership and reuse intent.
- [ ] Add the exact license text and update the README.
- [ ] Do not assume that synthetic data or generated code is automatically free of all third-party rights.

## Publication and remote verification
- [ ] Create a dedicated repository; do not reuse an unrelated personal or application repository.
- [ ] Push the reviewed commit.
- [ ] Confirm the default branch and repository visibility.
- [ ] Confirm GitHub Actions passes on the remote commit.
- [ ] Clone the remote repository into a new directory and rerun all commands.
- [ ] Record the remote commit SHA, CI run URL and clean-clone test output.

## Claims
Only describe work actually performed. Do not claim hospital deployment, real-patient analysis, causal findings, clinical validation, employer review or remote CI success without evidence.
