# Healthcare Data Analyst Academy — v5.60.3 maintenance release

**Feature baseline:** v5.60.0. **Current package:** v5.60.3. Feature development is paused while the cumulative academy is stabilised and used.

## Start here
1. Extract the ZIP to a writable folder.
2. Read `SHOWCASE.md`, `STABILIZATION_GUIDE.md` and `ACADEMY_CATALOG.md`.
3. Open `index.html` in Firefox or Chromium.
4. Use **Project library** to open existing project guides. Use Curriculum and the reference-centre sections for guided study.
5. Start career execution with `career_launch_kit_v555/README.md`, then follow v5.56 through v5.60.

## Main content
- Learning: Excel, SQL, Python, statistics, epidemiology, data visualisation, healthcare standards, ETL, databases and BI.
- Practice: clinical analytics, medication utilisation, synthetic outpatient operations, research methods, data quality and reporting.
- Engineering: reproducible pipelines, SQL modelling, dashboards, tests, data dictionaries, metric contracts and publication gates.
- Career: CV/LinkedIn preparation, job-fit analysis, interview practice, application tracking, vacancy verification and evidence capture.

## Maintained test command
Install pytest in the Python environment, then run from the academy root:

```bash
python -m pip install pytest
python -B -m pytest -q
```

This root command runs only the six maintained career release-gate suites; it is not a full-academy test. Run `python -B scripts/verify_full_academy.py --timeout 30 --jobs 2` to inventory and execute test directories independently. It writes `FULL_TEST_REPORT.json`, including passed, failed, timed-out and dependency/import-error statuses. Do not interpret a partial report as a full pass. See `MODULE_COMPATIBILITY_MATRIX.md` for the course-pack inventory.

## Dashboard browser acceptance
See `dashboard_uat_v550/README.md`. Its dedicated runner starts a local server and launches Playwright Chromium. A successful run on your Ryoku workstation is still required; the current build environment blocks browser navigation and cannot certify it.

## Data integrity
The real Pharm.D thesis, **Drug Utilization Evaluation of Antihypertensives in a Tertiary Care Teaching Hospital** (prospective observational, N=153), is distinct from all synthetic training projects. Do not merge the datasets or present fictional outputs as clinical findings. Never publish identifiable or institution-restricted patient data.

## External work not claimed
No live vacancies sourced, employers verified, applications submitted, GitHub publication pushed, hosted CI completed, PBIX delivered or recruiter contacted by this package.

See `RELEASE_NOTES_v5.60.3.md`, `CHANGELOG.md`, `STABILIZATION_REPORT.md`, `SECURITY.md`, `DATA_HANDLING_POLICY.md` and `LICENSE_DECISION_REQUIRED.md`.
