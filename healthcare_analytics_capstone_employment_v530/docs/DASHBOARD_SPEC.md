# Dashboard specification

1. Executive operations: distinct patients, total encounters, completed/cancelled status, monthly trend.
2. Pharmacy utilization: order count, drug-class mix, top medication names; avoid adherence claims.
3. Clinical observations: systolic/diastolic distributions and encounter-level paired values; label units and sample size.
4. Data quality: source row counts, duplicate keys, nulls, orphan patient/encounter references, refresh timestamp.

Use a date dimension and single-direction dimension-to-fact relationships. Keep observation and medication fact tables separate. Add a visible note that the dataset is synthetic and BP summaries are descriptive only.
