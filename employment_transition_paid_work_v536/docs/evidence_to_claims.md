# Evidence-to-claim mapping

Use this before every CV, LinkedIn, portfolio or interview claim.

| Claim type | Acceptable evidence | Safer wording | Avoid |
|---|---|---|---|
| Python | Runnable script, pinned dependencies, test output, sample input/output | “Built a Python/pandas workflow on synthetic encounter data; documented validation and exceptions.” | “Production Python engineer” |
| SQL | Query file, database engine/version, reproducible result and test | “Practised SQLite analytics queries; PostgreSQL scripts are prepared but deployment is pending.” | “Advanced PostgreSQL in production” |
| BI | PBIX/PBIP, screenshots, model measures, refresh evidence and QA | “Designed a Power BI dashboard specification” if no Desktop execution | “Delivered Power BI dashboards” |
| Healthcare domain | Pharm.D coursework and clearly identified academic projects | “Pharm.D candidate with clinical-pharmacy domain knowledge.” | “Clinical data analyst with hospital employment” |
| ETL | Source-to-target mapping, run log, rejected-row report, reconciliation | “Implemented a local synthetic-data ETL pipeline.” | “Enterprise data pipeline” |
| Impact | Baseline, method, measured outcome and independent context | State the measured result and its limitations | Invented savings, improved outcomes or client impact |

## Claim audit
For each sentence, record: exact claim; artifact path; command used; environment/version; date; result; limitation. If any field is missing, downgrade or remove the claim.

### Current Academy evidence boundary
- v5.32 is a synthetic practicum, not a real hospital deployment.
- v5.34 PostgreSQL environment was not executed in the build runtime; user-side execution is still needed.
- Power BI Desktop publication and GitHub public release are not evidenced by the Academy package itself.
- A passing unit test demonstrates only the tested behavior, not general professional readiness.
