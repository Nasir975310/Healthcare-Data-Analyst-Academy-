# Portfolio release checklist

- [ ] Re-run source pipeline from clean inputs.
- [ ] Run local evidence capture; inspect JSON, not just exit code.
- [ ] Run PostgreSQL Compose validation and retain evidence JSON.
- [ ] Build PBIX; reconcile each KPI to SQL; record application version and PBIX SHA-256.
- [ ] Inspect `.gitignore`, `git status`, staged diff and full commit history for secrets/PHI.
- [ ] Confirm synthetic data and asset licensing.
- [ ] Push to the intended public/private repository.
- [ ] Test README reproduction instructions from a clean clone.
- [ ] Run release gate; explain all PENDING checks.
- [ ] Tag release only after review.
