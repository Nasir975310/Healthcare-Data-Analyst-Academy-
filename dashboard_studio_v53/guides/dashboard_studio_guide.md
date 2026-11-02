# Healthcare Analytics Dashboard Studio — v5.3

## Workflow
1. Load the synthetic sample or upload a non-sensitive CSV.
2. Select a date field and optional date range.
3. Select a department filter.
4. Choose the row grain and metric definitions before charting.
5. Select a chart and metric.
6. Review the denominator, data-quality caveats and dashboard QA checks.
7. Export a self-contained HTML snapshot.

## Supported chart modes
- Bar: category comparison.
- Line: date trend grouped by day or month.
- Donut: composition of the selected metric.
- Table: inspect aggregated values.

## Metric cautions
- Encounter count is a row count only if the input is one row per encounter.
- Unique patients requires a stable patient identifier.
- Average LOS is meaningful only if LOS is defined and the cohort is appropriate.
- SBP completeness is a data completeness metric, not blood-pressure control.
- No causal or clinical quality conclusions are generated.

## Export
HTML export contains the current filtered summary and a chart rendered from the selected aggregation. Review the exported report and confirm data definitions before portfolio publication.
