# Validation methodology and interpretation

## Rule classes
- Completeness: required fields and blank-cell profiling.
- Uniqueness: duplicate checks for configured key columns.
- Type/format: numeric parsing, ISO dates and allowed categories.
- Range plausibility: configurable minimum/maximum screens.
- Temporal logic: ordering of index and follow-up dates.
- Cross-field logic: deterministic relationships between fields.

## Severity
Errors block a PASS result. Warnings are review signals and do not necessarily make a dataset invalid. A warning threshold is a technical rule, not a clinical reference interval.

## Important limitations
- The engine checks configured rules only; it cannot discover every possible data error.
- A clean report does not prove source accuracy, representativeness, absence of bias or clinical validity.
- Range checks must be approved for the actual population, device, units and protocol.
- Missingness percentages are descriptive; no imputation is performed.
- No hypothesis tests, sample-size calculations, causal inference or endpoint adjudication are performed.
- No PHI should be placed in teaching fixtures or uploaded to unapproved systems.
