# Healthcare Data Analyst Academy

**Offline-first learning academy · healthcare analytics portfolio toolkit · packaged baseline v5.60.3**

A practical course-pack for developing healthcare analytics capability across Excel, SQL, Python, statistics, data quality, ETL, databases, BI, reproducible reporting and career execution.

> **Repository status:** This GitHub repository currently contains the onboarding/governance scaffold; the complete 1,645-entry v5.60.3 source archive is **not yet imported into the Git tree**. See [repository import status](REPOSITORY_IMPORT_STATUS.md). The historical test audit is incomplete. Passing maintained tests do not certify every historical module. Browser acceptance on the target workstation is pending.

## Start here

1. Read [Getting started](GETTING_STARTED.md) and [Academy catalogue](ACADEMY_CATALOG.md).
2. Choose a route in [Learning paths](LEARNING_PATHS.md): beginner, SQL/BI, or Python/data engineering.
3. Open [index.html](index.html) for the offline academy interface.
4. Prioritise the synthetic outpatient analytics capstone as the flagship portfolio project.
5. Track actual evidence in [PROGRESS_TRACKER.md](PROGRESS_TRACKER.md).

## What is included

- Foundations: Excel, SQL, Python, statistics, epidemiology, visualisation and healthcare context.
- Analytics engineering: cleaning, validation, ETL, database design, reproducibility and reporting.
- BI: dashboard design, metric contracts, reconciliation and UAT materials.
- Portfolio projects: synthetic outpatient operations and medication-utilisation exercises, datasets, scripts, tests and reports.
- Career execution: role targeting, CV/LinkedIn materials, vacancy verification, application tracking, interviews and evidence capture.
- Governance: privacy, data handling, clinical safety boundaries and QA tooling.

This is a **course-pack repository**, not a single installable application. Modules may have distinct prerequisites; consult [MODULE_COMPATIBILITY_MATRIX.md](MODULE_COMPATIBILITY_MATRIX.md) and each module README.

## Verification status

The v5.60.3 stabilization report recorded 36 maintained tests and 11 unittest subtests passing, 208/208 Python AST checks, and successful release-document and configured sensitive-pattern checks at that release point. These are historical release results, not fresh GitHub Actions results.

The separate historical audit discovered 69 test directories. Latest progress snapshot:

| Status | Directories |
|---|---:|
| Passed | 33 |
| Timed out | 16 |
| No tests collected | 2 |
| Not run | 18 |

The sweep is **incomplete**. Timeouts are inconclusive, not passes. See [audit progress](FULL_TEST_AUDIT_PROGRESS_v5.60.3.md). The machine-readable detailed report is retained in the v5.60.3 audit artifact held with the release materials; it is not represented as a complete pass.

Resume the packaged audit from the academy root:
```bash
python -B scripts/verify_full_academy.py --timeout 30 --jobs 1 --resume --output FULL_TEST_REPORT.json
```

Review failed, timed-out, dependency/import, environment-blocked and no-tests results separately. Never relabel timeouts as passed.

## Flagship project and safety boundaries

Recommended route: **SQL/Python healthcare analytics → synthetic outpatient capstone → tested outputs → reproducible case study → public-safe portfolio**. Define every metric's population, numerator, denominator, exclusions and time window.

The real Pharm.D thesis, *Drug Utilization Evaluation of Antihypertensives in a Tertiary Care Teaching Hospital* (prospective observational, N=153), is separate from all synthetic academy projects. Do not mix thesis data with training data or publish patient-level or institution-restricted information.

No employment, employer review, clinical deployment, live vacancy verification, application submission, separate capstone publication, recruiter contact or remote CI success is claimed unless an inspectable record demonstrates it.

## Contributing, security and licensing

Read [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), [DATA_HANDLING_POLICY.md](DATA_HANDLING_POLICY.md) and [LICENSE_DECISION_REQUIRED.md](LICENSE_DECISION_REQUIRED.md). The repository includes an MIT License for original material the owner has the right to license. Third-party assets and datasets require separate provenance and license review; see [license guidance](LICENSE_DECISION_REQUIRED.md).
