# Analyst handoff

## What this project does
Runs a reproducible descriptive analysis of synthetic encounter data for 2026 Q1 using Python, with independent R and SQL reference implementations and a Quarto report source.

## Re-run checklist
1. Open the Academy root directory.
2. Activate the project virtual environment.
3. Install `requirements.txt`.
4. Run the Python CLI command in the project README.
5. Run automated tests.
6. If R is installed, run the R summary and visualization scripts.
7. Reconcile Python/R summaries with SQL using identical dates and denominators.
8. Render the Quarto report and inspect the HTML output.

## Expected control totals
- Source encounters: 104
- Unique encounter IDs: 104
- Q1 encounters: 104
- Distinct patients in Q1: 60
- Nonmissing SBP: 96
- Missing SBP: 8
- Unmatched department keys: 0
- Department encounter sum: 104

## Known limitations
R and Quarto execution were not validated in the build environment. The data are synthetic. The analysis is descriptive only and repeated encounters may be clustered within patients. Do not interpret department differences causally.

## Ownership and next action
A receiving analyst should first confirm the source file version and cohort dates, then rerun tests and reconcile totals before changing any metric definition or publishing a revised report.
