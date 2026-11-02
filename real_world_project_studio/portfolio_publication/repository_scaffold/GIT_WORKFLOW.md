# Git workflow (Linux/Fish and Windows PowerShell)

Run from the project repository root.

## First commit
```bash
git init
git status --short
git add README.md .gitignore docs src sql tests reports
git diff --cached --stat
git diff --cached
git commit -m "Initial reproducible healthcare analytics project"
```

PowerShell uses the same Git commands. Before staging any data folder, inspect every file and confirm that it is synthetic, public, or explicitly authorised. Never commit PHI, credentials, tokens, or restricted employer extracts.

## Branch and review
```bash
git switch -c feature/metric-validation
git status --short
git add .
git diff --cached
git commit -m "Add metric validation and tests"
git switch main
git merge --no-ff feature/metric-validation
```

## Clean reproduction
Create a fresh virtual environment, install declared dependencies, run scripts and tests, and compare regenerated outputs. Do not claim reproducibility solely because an existing notebook or local environment runs.
