# GitHub publication runbook

This is a user-executed procedure. Creating a local staging export does not publish it.

## 1. Build a focused repository export

From the Academy root:
```bash
python github_portfolio_publication_v542/src/build_public_repo.py \
  --source portfolio_execution_reproducibility_v538 \
  --destination /tmp/synthetic-outpatient-analytics \
  --case-study portfolio_evidence_pack_v540/CASE_STUDY.md
```

## 2. Inspect before publishing

```bash
python github_portfolio_publication_v542/src/publication_scan.py \
  --repo /tmp/synthetic-outpatient-analytics \
  --out /tmp/synthetic-outpatient-analytics/publication_scan.json

cd /tmp/synthetic-outpatient-analytics
find . -maxdepth 4 -type f -print | sort
git diff --no-index /dev/null README.md
```

A zero-finding scan is not security certification. Manually inspect all files, history, screenshots, data provenance and licensing. The generated scanner is heuristic and may miss secrets or personal information.

## 3. Initialize and inspect Git

```bash
git init
git branch -M main
git status --short
git add .
git diff --cached --stat
git diff --cached
```

Do not commit if any real patient information, confidential data, credentials, private keys or unauthorized material is present. Ensure generated SQLite files and local outputs are ignored.

## 4. Create a GitHub repository

Using GitHub CLI:
```bash
gh auth status
gh repo create synthetic-outpatient-operations-analytics --public --source=. --remote=origin
```

If you prefer a private repository, create it as private in the GitHub UI or use `--private` instead of `--public`. Decide visibility deliberately. Do not publish merely to satisfy a checklist.

## 5. Push and verify

```bash
git push -u origin main
gh repo view --json nameWithOwner,url,visibility
```

Then perform a fresh-clone reproduction:
```bash
cd /tmp
git clone <YOUR_REPOSITORY_URL> synthetic-outpatient-clean-clone
cd synthetic-outpatient-clean-clone
python --version
python src/run_project.py
python -m unittest discover -s tests -v
python scripts/repository_preflight.py
```

Record repository URL, commit hash, visibility, clone date, environment, commands, exit codes and outputs in `templates/PUBLICATION_EVIDENCE.md`.

## 6. License decision
No license is automatically applied. Choose one only after confirming ownership/permission for all code, text and data. A public GitHub repository without a license does not automatically grant broad reuse rights.

## What this runbook cannot do
It cannot create an account, authenticate, choose public/private visibility for you, publish to GitHub, or verify a live remote. Those actions require your explicit account interaction.
