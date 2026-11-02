# Production acceptance plan

## Definition of done
1. Reproducible source ingestion with a manifest and immutable raw inputs.
2. Explicit staging-to-curated rejection rules; no silent row drops.
3. Referential integrity and key uniqueness checks.
4. KPI reconciliation from source through curated model to dashboard.
5. Least-privilege access, no secrets in source control, synthetic/public data only.
6. Dashboard usability, refresh, filter, accessibility and performance checks.
7. Reproducible run instructions, limitations, evidence and handover.
8. Client acceptance signed against measurable criteria.

## Release gates
| Gate | Pass condition | Evidence |
|---|---|---|
| Data quality | Critical checks pass; exceptions explained | validation JSON/CSV |
| Reconciliation | Source counts = accepted + rejected | reconciliation output |
| Analytics | KPI definitions and grain documented | KPI dictionary and SQL |
| BI | Measures reconcile to SQL within stated tolerance | exported QA workbook/screenshots |
| Security | No PHI, secrets, public write access or excessive permissions | repository and access review |
| Performance | Refresh and interaction budgets met on target hardware | timed test log |
| Delivery | Reproducible setup and client handover | README, changelog, demo |

## Error patterns and corrective actions
- Duplicate business keys: define canonical key, quarantine duplicates, resolve source precedence.
- Orphan facts: preserve raw row, route to exception table, fix upstream mapping; never silently delete.
- Unit/timezone drift: normalize units and timestamps at ingestion; retain original values.
- KPI mismatch: align grain, date window, inclusion rules, null handling and distinct-count logic.
- Dashboard slow: reduce cardinality, remove unused columns, pre-aggregate, use star schema, inspect query plans.
- Accidental PHI exposure: stop publication, revoke access/tokens, notify responsible owner, follow incident process.
- Hard-coded credentials: rotate immediately, use environment/secret manager, scan history.
- Misleading clinical interpretation: label descriptive statistics and avoid causal/diagnostic claims without valid design.
