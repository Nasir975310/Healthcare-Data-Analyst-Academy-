# Synthetic simulation datasets

All data in this directory are generated for training and contain no real patient records.

| File | Rows | Grain | Purpose |
|---|---:|---|---|
| encounters_raw.csv | 501 | Intended one row per encounter; one duplicate injected | Hospital operations and data-quality review |
| medication_orders_raw.csv | 1,000 | One row per synthetic medication order | Join, reconciliation and order quality |
| antihypertensive_due_cohort.csv | 300 | One synthetic study participant | Descriptive DUE analysis |

Intentional issues include duplicate encounter key, missing dimensions, invalid payer, negative length of stay, discharge before admission, orphan order reference, non-positive quantities, missing cost/class, implausible age, missing follow-up SBP and invalid follow-up interval. Do not silently clean these; document issue counts, exclusions and denominator changes.
