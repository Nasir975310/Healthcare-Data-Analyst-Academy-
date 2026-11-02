# Publish the practicum as a portfolio repository

## Before publication
- [ ] Confirm every dataset is synthetic or licensed for redistribution.
- [ ] Remove database files, logs, caches, credentials, tokens and local paths.
- [ ] Review CSVs and screenshots for direct/indirect identifiers.
- [ ] Add `LICENSE` only after confirming ownership and dependency licenses.
- [ ] Add `README.md`, data dictionary, KPI dictionary, reproducible run steps and limitations.
- [ ] Include test outputs and SHA-256 manifest.
- [ ] State clearly this is an academic synthetic project, not employment or a real hospital engagement.

## Suggested repository layout
```
healthcare-analytics-practicum/
  README.md
  data/sample/
  src/
  sql/
  powerbi/
  docs/
  tests/
  evidence/
  .gitignore
```

## Safe Git sequence
```bash
git init
git status --short
git add README.md docs src sql powerbi tests
git diff --cached --stat
git diff --cached
git commit -m "Build synthetic healthcare analytics practicum"
git branch -M main
# Add your own remote URL after creating a repository.
git remote add origin YOUR_REPOSITORY_REMOTE
git push -u origin main
```
Do not paste tokens into commands or commit `.env` files. Use SSH or the official Git credential manager. Inspect `git status` and staged diff before every push.
