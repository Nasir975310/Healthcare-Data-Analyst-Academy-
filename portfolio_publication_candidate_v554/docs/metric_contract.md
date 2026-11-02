# Metric contract

## Completed encounter volume
- **Grain:** one deduplicated encounter.
- **Numerator:** rows where status is `completed`.
- **Eligibility:** valid ISO encounter date and nonblank department.
- **Deduplication:** first occurrence of encounter_id retained in this teaching fixture.
- **Interpretation:** count of eligible completed encounter records; not unique patients.

## Mean recorded wait (minutes)
- **Population:** eligible completed encounter records.
- **Numerator:** sum of numeric nonnegative wait_minutes.
- **Denominator:** number of eligible records with numeric nonnegative wait_minutes (`valid_wait_n`).
- **Missing/invalid:** missing wait excluded from the mean; negative values excluded and reported as exceptions.
- **Interpretation:** arithmetic mean of recorded waits, not a service-level compliance metric.

## Guardrails
Do not label cancelled/no-show rows as completed visits. Do not treat missing wait as zero. Do not infer patient outcomes, quality of care or causality. If the duplicate-resolution rule changes, document and revalidate all outputs.
