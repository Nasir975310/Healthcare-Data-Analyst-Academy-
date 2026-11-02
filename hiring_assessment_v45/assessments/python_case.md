# Stage 3 — Python and data-quality case (30 minutes)

A CSV contains encounter IDs, dates, department, length of stay and a supplied outcome flag.

Tasks:
1. Load without overwriting the raw file.
2. Report shape, types, missingness and duplicate keys.
3. Validate date chronology and LOS plausibility.
4. Preserve invalid rows in an exception file with reason codes.
5. Produce department summaries with explicit denominators.
6. Save a run log and concise limitations note.

Explain why `fillna(0)` is not a universal missing-data strategy and why a supplied outcome flag must be validated before being labelled a clinical outcome.
