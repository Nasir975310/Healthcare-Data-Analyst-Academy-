# Client brief: fictional regional hospital

The hospital operations lead requests a reproducible monthly activity and medication-utilization report. The quality team also wants assurance that source data can be reconciled before any dashboard is trusted.

## Your assignment
- Profile all four source tables and document row counts, keys, nulls, duplicates and referential integrity.
- Build a relational model with explicit grain.
- Produce monthly encounters, encounter-type mix, medication class utilization and descriptive BP summaries.
- Reconcile source and warehouse counts.
- Design a four-page dashboard: executive operations, pharmacy utilization, observations, and data quality.
- Write an executive summary with limitations and actionable next data requests.

## Required outputs
`data_quality_report`, `data_dictionary`, `model_diagram`, `SQL_queries`, `KPI_dictionary`, `dashboard_mockup`, `executive_summary`, `technical_handover`.

## Constraints
All input data are fictional. Do not infer diagnosis, treatment appropriateness, adherence, outcomes or guideline compliance from this dataset. Explain missing fields and the deliberately orphaned encounter.
