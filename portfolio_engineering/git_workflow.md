# Git and GitHub workflow for healthcare analytics projects

## 1. Initialise locally
```bash
mkdir my-healthcare-project
cd my-healthcare-project
git init
git branch -M main
```

## 2. Create a safe project structure
```text
my-healthcare-project/
├── README.md
├── .gitignore
├── requirements.txt
├── data/
│   ├── raw/          # synthetic/sample or approved, never PHI
│   └── processed/
├── src/
├── sql/
├── tests/
├── reports/
└── docs/
```

## 3. Inspect before staging
```bash
git status --short
git diff
git diff --check
```
Add selected files rather than blindly staging all files:
```bash
git add README.md src/ tests/ docs/
git diff --cached --stat
git diff --cached
```
Check for identifiers, confidential client data, credentials, local databases and large generated files. The provided preflight script is an additional check, not a substitute for inspection.

## 4. Commit a coherent change
```bash
git commit -m "Add encounter quality validation"
git log --oneline --decorate -5
```
Prefer one logical change per commit. Do not rewrite shared history without agreement.

## 5. Feature branch and review
```bash
git switch -c feature/monthly-kpi-validation
# make and test a focused change
git diff
git add src/ tests/
git commit -m "Validate monthly KPI denominators"
```
For a hosted review, create a pull request only after repository visibility and data permissions are confirmed. Keep PR scope small and use the supplied PR template.

## 6. Add a remote cautiously
GitHub CLI example:
```bash
gh auth status
gh repo create my-healthcare-project --private --source=. --remote=origin --push
```
This creates a private repository only if your account and CLI are authorised. Check the target repository and visibility before pushing. Private does not mean authorised for patient data. Do not publish PHI or confidential client extracts.

## 7. Recover from common mistakes
- Unstaged changes: `git status`, `git diff`.
- Staged wrong file but not committed: `git restore --staged path/to/file`.
- Discard local change only when certain: `git restore path/to/file` (destructive to that uncommitted change).
- Inspect a commit: `git show --stat --oneline HEAD`.
- Never push secrets then assume deleting the file from the latest commit removes exposure. Revoke/rotate the secret and follow incident response.

## Fish shell note
Git commands are the same in Fish. Activate Python virtual environments with:
```fish
source .venv/bin/activate.fish
```

## PowerShell note
Commands above generally work in PowerShell with Git for Windows installed. Python activation:
```powershell
.\.venv\Scripts\Activate.ps1
```
Execution policy may affect activation; use an approved policy, not an arbitrary bypass.
