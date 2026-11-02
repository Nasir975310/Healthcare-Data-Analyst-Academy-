# Simulated client review and change request

This is a fictional practice scenario.

## Initial feedback from operations lead
"The monthly encounter chart looks useful, but I need scheduled visits separated from completed visits. The data-quality section mentions one orphan patient reference. Please show the rejected record count and do not hide it."

## Change request from pharmacy lead
"Please label the chart as medication orders by class. It must not say medication use, adherence or dispensing because these extracts only represent orders."

## Change request from data-quality coordinator
"Please provide a source-to-curated reconciliation and identify the encounter ID that was rejected. Keep the raw source row available in staging."

## Required revision log
| Change | Requested by | Evidence of completion |
|---|---|---|
| Separate scheduled/completed/cancelled | Operations | Updated KPI and chart |
| Correct medication label | Pharmacy | Updated title and KPI dictionary |
| Expose rejected encounter count and key | Data quality | Exception report and reconciliation |
| Preserve raw staging row | Data engineering | Staging query result |

## Acceptance decision
Mark accepted only after each change is implemented, retested and documented. If a request cannot be met, record the reason and obtain explicit client agreement.
