# v5.42.0 — GitHub Portfolio Publication Preparation

This release prepares a focused, reviewable repository for the v5.38 synthetic outpatient analytics project. It creates a local staging export; it does not publish to GitHub.

## Included
- Safe export builder that refuses to overwrite a non-empty destination.
- Generated repository README, GitHub Actions workflow and SHA-256 source manifest.
- Conservative secret / unsafe-artifact scanner.
- GitHub CLI publication runbook, privacy/provenance checklist, license worksheet and evidence template.
- Actual `sample_export/` built from the current v5.38 project, with the populated v5.40 case study.
- Automated tests and a sample scanner report.

## Build your own staging export
From the Academy root:
```bash
python github_portfolio_publication_v542/src/build_public_repo.py \
  --source portfolio_execution_reproducibility_v538 \
  --destination /tmp/synthetic-outpatient-analytics \
  --case-study portfolio_evidence_pack_v540/CASE_STUDY.md
```

Run the scanner:
```bash
python github_portfolio_publication_v542/src/publication_scan.py \
  --repo /tmp/synthetic-outpatient-analytics \
  --out /tmp/synthetic-outpatient-analytics/publication_scan.json
```

Read `docs/GITHUB_PUBLICATION_RUNBOOK.md` before any GitHub action.

## Actual status
The local sample export was built and its scanner returned zero heuristic findings. Its tests passed 5/5. This is not a complete manual privacy/legal review. No license was selected, no GitHub repository was created or pushed, no live Actions run occurred, and no fresh clone from GitHub was tested.
