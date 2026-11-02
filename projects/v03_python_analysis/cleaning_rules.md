# Data-cleaning rules and interpretation guide

## Input and grain
- Source: `datasets/v03_python/encounters.csv`.
- Grain: one row per encounter.
- Preserve the raw CSV unchanged.
- Keep identifiers as strings; they are labels, not quantities.

## Rules
1. Required columns must exist before processing.
2. `encounter_id` must be nonmissing and unique in the encounter-grain file.
3. `admission_date` must parse using the documented ISO `YYYY-MM-DD` format.
4. Blank SBP is missing; it must not be converted to zero.
5. Nonblank SBP values that fail numeric parsing must be flagged.
6. Discharge before admission is flagged for review, not silently corrected.
7. Extreme numeric values are flagged for source/domain review; no automatic deletion is authorized.
8. Every excluded or quarantined row must be counted and explained.

## Disposition
- Fatal structural failure: stop the pipeline and correct the input or mapping.
- Record-level defect: retain in a flagged output and seek source review.
- Missing SBP: retain the encounter; exclude only from metrics requiring SBP and report the denominator.
- Outlier: investigate context and units; do not delete based on an arbitrary threshold.

## Reporting
Report input rows, output rows, flagged rows, missingness, duplicate key counts, parsing failures and all transformations. Never overwrite the raw source.
