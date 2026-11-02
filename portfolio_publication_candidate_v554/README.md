# Synthetic Outpatient Operations Analytics

A reproducible healthcare analytics portfolio project using **fictional, synthetic outpatient encounter data**. It demonstrates a practical analyst workflow: inspect data quality, define operational metrics, analyze department-level waiting times, and produce auditable outputs using Python, SQL and CSV.

> **Data and safety notice:** Every record in this repository is synthetic. This is an educational portfolio demonstration, not patient data, clinical evidence, a validated hospital performance study, or a clinical decision-support tool. Do not use the outputs to make care or staffing decisions.

## Project question

How do data-quality exclusions affect the interpretation of outpatient waiting-time summaries across departments?

## What this project demonstrates

- Data inspection and reproducible cleaning rules.
- Explicit metric definitions and denominators.
- Python standard-library data processing.
- SQL aggregation and exception analysis.
- Reconciliation of raw, deduplicated, eligible and analyzable records.
- Machine-readable quality outputs and SHA-256 manifests.
- Automated tests and GitHub Actions CI.

## Quick start

Requirements: Python 3.10 or newer. No third-party Python packages are required.

```bash
python src/run_project.py
python -m unittest discover -s tests -v
python scripts/repository_preflight.py
```

Generated files are written under `outputs/`. The project includes reference outputs for comparison; rerunning the pipeline may refresh generated artifacts.

## Repository map

```text
.
├── data/                  # Synthetic encounter CSV
├── docs/                  # Data dictionary, metric contract, reference results
├── outputs/               # Reproducible summaries and quality reports
├── sql/                   # SQL analysis queries
├── src/                   # Python analysis pipeline
├── tests/                 # Automated tests
├── scripts/               # Repository hygiene preflight
├── .github/workflows/     # GitHub Actions test workflow
├── CASE_STUDY.md          # Problem, method, findings and limitations
└── SOURCE_MANIFEST.json   # Source file hashes
```

## Analytical guardrails

- Waiting-time summaries use only records that satisfy the eligibility and validity rules in `docs/metric_contract.md`.
- Missing or invalid values are not silently converted to zero.
- Department comparisons are descriptive, not causal.
- Small synthetic group sizes should not be generalized to real hospitals.
- The included data are intentionally constructed for learning and do not represent any institution or patient population.

## Reproducibility and review

See:
- `docs/data_dictionary.md`
- `docs/metric_contract.md`
- `docs/reference_results.md`
- `docs/reproduction_and_review.md`
- `QA_REPORT.md`

The GitHub Actions workflow runs the project tests on pushes and pull requests. A successful local run does not prove that remote CI has run; remote status is visible only after publishing the repository.

## License

No license is asserted by this package. Before making the repository public, choose and add a license only after reviewing the rights and intended reuse. Without a license, default copyright restrictions apply. See `PUBLICATION_REVIEW.md`.

## Suggested portfolio description

Built a reproducible synthetic outpatient operations analytics project using Python, SQL and automated tests. Implemented explicit data-quality rules, metric definitions, department-level descriptive summaries, reproducibility checks and CI configuration. All data are fictional; results are not clinical evidence.
