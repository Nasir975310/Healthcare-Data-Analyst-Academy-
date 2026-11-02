# ENG-04 — Medication-order reconciliation and dashboard incident

**Client:** Fictional data engineering and BI team  
**Decision:** Why did the medication dashboard's encounter metrics change after a data model update?  
**Grain:** Encounters are one row per encounter; medication orders are one row per order.

## Request
Investigate the supplied encounter and medication-order files. Identify unmatched order references, invalid quantities, missing unit costs/classes, and join fan-out. Rebuild a safe summary that preserves encounter grain.

## Required deliverables
1. Key uniqueness and referential-integrity checks.
2. Order exception/quarantine file with reason codes.
3. Safe encounter/order summary using pre-aggregation or separate measures.
4. Before/after row-count reconciliation.
5. Short root-cause report and reproducible SQL/Python.

## Acceptance criteria
- Never use `DISTINCT` as an unexplained repair.
- Quantify unmatched orders and invalid/missing fields.
- Demonstrate how one-to-many joins change row counts.
- Keep encounter and order counts separately defined.
- Document whether excluded rows are quarantined, repaired or retained.
