# Release notes — v5.50.0

## Scope
Dashboard user acceptance testing and portfolio integration. The release adds a repeatable Playwright test suite and evidence workflow around the synthetic clinical BI dashboard.

## QA performed in build environment
- UAT asset tests: 3 passed.
- Playwright browser suite: skipped because the Chromium browser binary is not installed in this build environment. This is not counted as a pass.
- v5.49 dashboard Python tests: 8 passed.
- v5.49 independent reconciliation: 73 filter cases generated from 301 synthetic rows.
- Dashboard JavaScript syntax: passed with Node.js.
- Archive integrity and forbidden-artifact scan: performed at packaging.

## Explicitly not verified
- Browser interaction on the user's Ryoku laptop.
- CSV opening in ONLYOFFICE/LibreOffice/Excel on the user's workstation.
- GitHub publication, remote CI, clean-clone verification, Power BI PBIX, employer review, or clinical deployment.

## User's next action
Follow `dashboard_uat_v550/README.md`, run the Playwright browser suite, and inspect the generated `dashboard_uat_v550/evidence/uat_result.json`.

All case-study data remains synthetic and separate from the user's Pharm.D thesis dataset.
