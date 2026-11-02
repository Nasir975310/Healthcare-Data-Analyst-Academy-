# Power BI client handoff

## Deliverables
- [ ] Power BI Desktop `.pbix`
- [ ] PDF export
- [ ] Source data extracts / source location
- [ ] Metric dictionary
- [ ] Data model / relationship specification
- [ ] QA log and reconciliation results
- [ ] Refresh instructions

## Executive summary
Describe the reporting period, population, principal measures and any meaningful descriptive differences. Do not imply causation.

## Metric definitions
| Metric | Definition | Numerator / denominator | Unit | Source grain |
|---|---|---|---|---|
| Encounter count | Distinct encounter IDs | N/A | Encounters | Encounter |
| Mean LOS | Average supplied length_of_stay_days | Sum LOS / nonblank encounter count | Days | Encounter |
| Supplied readmission flag proportion | Sum of supplied flag / nonblank encounter metric rows | Flag / encounter rows | % | Encounter |
| Medication order count | Count of source order rows | N/A | Orders | Order |
| Ordered quantity | Sum of ordered quantity | N/A | Quantity units | Order |
| Synthetic order value | Sum(quantity × synthetic unit cost) | Missing-cost rows excluded | INR | Order |

## Data quality and limitations
- Synthetic data only.
- Supplied readmission flag is not independently validated.
- Medication orders do not prove dispensing, administration, adherence or appropriateness.
- Synthetic costs are not actual procurement prices.
- List missing, orphan and duplicate-candidate records and explain disposition.

## Validation
| Check | Expected | Actual | Pass / fail | Notes |
|---|---:|---:|---|---|
| Encounter rows | 80 | | | |
| Order rows | 151 | | | |
| Orphan order encounter references | 1 | | | |
| Missing unit cost | 1 | | | |
| Blank therapeutic class | 1 | | | |
| Ordered quantity | 3,038 | | | |

## Refresh procedure
List source paths, Power Query refresh steps, credentials (never include secrets), model refresh, and report export steps.

## Known issues and next actions
Record unresolved source quality issues, definition decisions, owner and due date.
