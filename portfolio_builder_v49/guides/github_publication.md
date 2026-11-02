# Git and GitHub publication workflow

1. Review all files and remove databases, caches, `.env`, secrets and private paths.
2. Confirm that only synthetic or explicitly authorised data is included.
3. Add a `.gitignore` and a clear README.
4. Run the project from a clean environment.
5. Run tests and record actual results.
6. Inspect `git status` and `git diff` before staging.
7. Commit with a descriptive message.
8. Create a public repository only after confirming that no confidential data or credentials are present.
9. Push using GitHub CLI or VS Code only after reviewing the target repository and visibility.
10. Re-open the repository as a visitor and verify the README, file links and reproduction instructions.

Commands (run inside your project folder):
```bash
git init
git status
git add README.md src tests sql data/raw reports
git diff --cached --stat
git commit -m "Add reproducible healthcare analytics project"
gh auth status
gh repo create healthcare-encounter-analytics --public --source=. --remote=origin --push
```
The final command creates a public repository. Do not run it until you have reviewed the staged content and deliberately chosen public visibility. For Windows, the same Git commands work in PowerShell when Git and GitHub CLI are installed.
