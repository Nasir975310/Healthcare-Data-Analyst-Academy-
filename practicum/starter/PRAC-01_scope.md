# PRAC-01 — Hospital performance review: starter pack

**Client:** COO and quality office  
**Timebox:** 5 working days  
**Question:** Is General Medicine's length of stay higher, and is medication workload increasing?

## Required first response
Before analysis, write a scope note that clarifies reporting dates, encounter grain, LOS definition, readmission flag definition, order-vs-administration distinction, missing-cost handling, audience and acceptance criteria.

## Data inventory
- `../data/encounters.csv`: one row per synthetic encounter.
- `../data/medication_orders.csv`: one row per synthetic medication order line.
- 32 intentionally orphan order references; missing unit costs are intentional.

## Required output
Metric dictionary, data-quality log, monthly/department KPI table, reproducible SQL or Python, executive memo, dashboard wireframe and limitations register.

## Definition reminders
- Mean LOS = sum of encounter LOS / eligible encounters.
- Order lines per encounter = order lines / encounters; do not imply administrations.
- Supplied readmission flag rate = flagged encounters / all supplied encounters unless a confirmed eligibility rule changes the denominator.
- Report the supplied flag as unvalidated.
