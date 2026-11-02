# Metric dictionary

- **Encounter count:** count of unique encounter IDs in the selected period.
- **Distinct patient count:** count of unique patient IDs linked to eligible encounters; not interchangeable with encounter count.
- **Mean length of stay:** arithmetic mean of the supplied encounter-level LOS; transfers and operational rules would require explicit definitions in real data.
- **Generic-name documentation percentage:** order rows with generic flag = 1 divided by all eligible order rows × 100. This is a synthetic documentation indicator, not a WHO prescribing indicator unless its formal sampling and definition requirements are met.
- **Medication class share:** orders in a class divided by all eligible medication order rows × 100.
- **Laboratory result completeness:** valid, non-cancelled results divided by expected results only if an expected-test denominator is available. This dataset does not provide an order table, so it supports result profiling but not a true completion rate.
- **Discharge status distribution:** encounters grouped by recorded synthetic status. Not a hospital mortality metric or quality comparison.
