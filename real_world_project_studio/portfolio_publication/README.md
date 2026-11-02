# Portfolio Publication Suite — v4.0

This folder packages the v3.9 synthetic engagements into hiring-manager-readable case studies and static, offline HTML dashboards.

## Build dashboards
From `real_world_project_studio/`:
```bash
python scripts/run_all.py
python portfolio_publication/scripts_dashboard_build.py
python -m unittest discover -s portfolio_publication/tests -v
```
Open the three HTML dashboards in a browser or from the academy local server.

## Deliverables
- Three standalone HTML dashboards with visible interpretation boundaries.
- Three concise case studies with source scope, method, results and limitations.
- Automated project data/output checks.
- Repository README, `.gitignore` and Git workflow templates.
- Interactive academy publication checklist and module backup/import.

## Publication gate
Before making a repository public, inspect all staged files. Training records are synthetic. If substituting real data, obtain explicit authorisation and use an approved secure environment. Do not upload PHI, patient-level extracts, credentials, or confidential employer information.
