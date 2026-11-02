# Dashboard specification and acceptance criteria

## Page 1 — Executive operations
Cards: patients, encounters, completed encounters, medication orders. Trend: monthly encounters. Breakdown: encounter type. Add a visible synthetic-data banner and refresh timestamp.

## Page 2 — Pharmacy utilization
Bar chart: medication orders by drug class and medication. Show denominator and distinct order count. Do not label order volume as adherence, appropriateness or consumption.

## Page 3 — Clinical observations
Show mean systolic/diastolic readings, reading counts and distribution by encounter date. Display units (mmHg), sample size, missingness and descriptive-only disclaimer. Avoid patient-level public display.

## Page 4 — Data quality
Show duplicate keys, orphan references, missing required fields, invalid numeric values and source freshness. All zero-error assertions must be backed by query results.

## Acceptance tests
1. Totals reconcile to source row counts and distinct keys.
2. Slicers filter intended dimensions only; test cross-filter direction.
3. Fact tables are not joined directly to each other.
4. Date table is marked as date table; date relationship is active.
5. RLS allowed and denied identities are tested with View As.
6. Exported visuals reconcile with detail-level query results.
7. Performance Analyzer is used to capture slow visuals; record before/after.
8. No real patient identifiers or data are present in the portfolio.
