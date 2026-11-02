# Interpreting the release gate

## PASS
All three commands recorded by the capture utility exited with code zero; each required output exists locally and in the reference set; local SHA-256 values match the reference; captured hash declarations are valid; environment metadata exists.

This supports a reproducible local execution claim for the captured project state. It does not prove that the code came from a public clean clone, that no sensitive data exist elsewhere in the repository, or that the learner can independently explain the work.

## REVIEW_REQUIRED
Inspect each failed check:
- nonzero command: read stdout/stderr and fix the execution problem;
- missing artifact: rerun the capture utility and confirm the pipeline output directory;
- invalid declared hash: do not edit the report manually; regenerate evidence;
- output mismatch: compare source CSV, code revision, Python version and output definitions. Explain legitimate differences; do not force a match.

## NOT_RUN
No local_run_report.json exists. This is the expected state until the user runs v5.40 locally and provides the captured evidence.

## Exact-match limitation
The comparator uses exact SHA-256 equality for quality JSON, department CSV and the manifest. If platform-specific or intentionally changed outputs differ, this conservative gate reports REVIEW_REQUIRED. A reviewer must inspect and approve a documented deviation rather than silently weakening the check.
