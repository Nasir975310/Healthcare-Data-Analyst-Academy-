# Practical data workflow

1. Preserve the raw source and record its origin, extraction time and grain.
2. Profile keys, missingness, distinct values, data types, ranges and date validity.
3. Define cleaning rules with the data owner; do not infer values without an approved rule.
4. Preview exclusions and reconcile raw = accepted + quarantined.
5. Define every KPI's numerator, denominator, unit, period and inclusion criteria.
6. Execute SQL in DBeaver/SQLite and reconcile query results to the source.
7. Review distributions, missingness and assumptions before statistical interpretation.
8. Build a dashboard with visible filters, denominators, freshness and limitations.
9. Export a reproducible report and retain code, queries and QA evidence.

The workbench's profiling heuristics are a first-pass aid, not a full data-quality framework.
