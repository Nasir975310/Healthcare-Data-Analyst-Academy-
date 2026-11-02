# Portfolio case study — Synthetic outpatient operations analytics

<small>Evidence-backed reference run · Academy v5.40.0 · synthetic teaching data</small>

## Executive summary

Built a reproducible Python/SQLite workflow that validates encounter-level outpatient records and produces department-level operational summaries. The included reference execution processed **24 source rows**, removed **1 duplicate encounter ID**, retained **23 unique records**, and identified **20 eligible completed encounters**. Of those, **18** had valid non-negative wait-time values.

This is a technical demonstration using synthetic data. It is not a real hospital performance evaluation and does not support clinical or causal conclusions.

## Business question and scope

**Question:** How can encounter records be transformed into transparent, quality-checked summaries of completed outpatient volume and mean recorded wait time by department?

**Audience:** A hypothetical outpatient operations analyst or manager.

**In scope:** duplicate identification, basic field validation, eligibility rules, missing/invalid wait-time handling, SQLite storage, department summaries and reproducible outputs.

**Out of scope:** patient outcomes, clinical effectiveness, service-level compliance, causal drivers, staffing optimization and real-world generalizability.

## Data and grain

- Source: `../portfolio_execution_reproducibility_v538/data/synthetic_outpatient_encounters.csv`
- Provenance: synthetic teaching fixture created for this Academy.
- Grain: one source row per encounter record.
- Expected unique key after deduplication: `encounter_id`.
- Fields include encounter and patient identifiers, department, date, status, wait minutes and source system.

## Method and metric contract

1. Read the CSV and validate required columns.
2. Retain the first occurrence of each `encounter_id`; flag later occurrences as duplicates.
3. Mark quality exceptions such as missing department and negative wait.
4. Define eligible completed encounters as deduplicated records with `status=completed`, a valid encounter date and nonblank department.
5. Calculate mean wait only among eligible records with numeric `wait_minutes >= 0`.
6. Store the deduplicated encounter table in SQLite and export quality JSON, department CSV and a SHA-256 manifest.

**Important denominator distinction:** completed encounter volume and valid wait-time sample size are not interchangeable. The General Medicine summary has 7 eligible completed encounters but only 5 valid wait observations.

## Reference execution results

| Measure | Result |
|---|---:|
| Raw rows | 24 |
| Duplicate rows removed | 1 |
| Deduplicated rows | 23 |
| Eligible completed encounters | 20 |
| Completed encounters with valid wait | 18 |
| Status: completed / cancelled / no-show | 21 / 1 / 1 |

### Department results

| Department | Eligible completed | Valid wait n | Mean wait (minutes) |
|---|---:|---:|---:|
| Cardiology | 7 | 7 | 21.29 |
| General Medicine | 7 | 5 | 32.60 |
| Orthopaedics | 6 | 6 | 33.67 |

These values are reproduced in `evidence/reference_run/department_summary.csv` and `quality_report.json`.

## Data-quality findings

- Duplicate encounter ID: `C023` (one duplicate row removed).
- `C014`: negative wait value; excluded from valid wait-time calculation.
- `C016`: missing department; excluded from eligible completed volume under the stated rule.
- The difference between 20 eligible completed encounters and 18 with valid wait is due to invalid/missing wait observations under the metric definition.

## Technical implementation and QA

- Python standard-library pipeline and SQLite table with primary key on `encounter_id`.
- SQL analysis reference and automated tests in the v5.38 project.
- Reference pipeline exit code: 0.
- v5.38 regression tests: 5/5 passed in the release build environment.
- Captured reference artifacts: `quality_report.json`, `department_summary.csv`, `sha256_manifest.json`, pipeline stdout and test log.

The evidence describes a run performed in the Academy release build environment. It is not evidence that the same commands have already been run on the learner's CachyOS workstation.

## Limitations and risks

- All records are synthetic; no inference about a real hospital is valid.
- Small fixture; no inferential statistics or stable trend conclusions.
- First-occurrence duplicate retention is a demonstration rule. Production systems require a source-authoritative version and correction policy.
- Mean is sensitive to outliers and missingness; median and distributional summaries may be more informative.
- No arrival/departure timestamps, appointment schedules, service targets or case-mix adjustment.
- No Power BI report, production database, access-control model or live integration is included.

## Next steps before public portfolio publication

1. Reproduce from a fresh clone or clean extracted copy on the learner's own machine.
2. Capture the local Python version, commands, exit codes and output hashes.
3. Reconcile the new local output with the reference output; explain any differences.
4. Manually inspect the repository for PHI/PII, credentials and licensing issues.
5. Add a genuine screenshot only if a real dashboard is subsequently built and executed.
6. Ask an independent reviewer to challenge the metric definitions and code.

## Evidence index

| Claim | Evidence |
|---|---|
| Row reconciliation and metric definitions | `evidence/reference_run/quality_report.json` |
| Department means and valid n | `evidence/reference_run/department_summary.csv` |
| Output integrity hashes | `evidence/reference_run/sha256_manifest.json` |
| Captured pipeline output | `evidence/reference_run/pipeline_stdout.json` |
| Regression test result | `evidence/reference_run/test_run.txt` |
| Re-run instructions | `docs/LOCAL_REPRODUCTION.md` |

**Portfolio claim boundary:** This demonstrates a synthetic analytics workflow and its QA. It does not establish paid experience, independent employer endorsement or proficiency with production hospital systems.
