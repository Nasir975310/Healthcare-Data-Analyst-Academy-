# Client communication simulation

Use the interactive simulator to respond to each message. Your decisions should be recorded before revealing the recommended response.

## Good delivery pattern
1. Restate the question and grain.
2. Confirm the denominator, time window and exclusions.
3. Profile raw data before cleaning.
4. Preserve raw input and quarantine invalid rows with reason codes.
5. Reconcile row counts and validate metric calculations.
6. Communicate caveats and obtain sign-off for ambiguous rules.
7. Deliver code, SQL, QA log and a concise summary.

## Escalation examples
- A duplicate key is not automatically a duplicate encounter; inspect source lineage before deduplicating.
- Missing department must not be guessed from patient or encounter context without an approved mapping.
- LOS definitions vary. Here it is calendar-day difference, not hours divided by 24.
- SBP completeness is a data completeness metric, not blood-pressure control or care quality.
