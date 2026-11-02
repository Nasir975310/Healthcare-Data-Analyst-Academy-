# Interactive Healthcare Analytics Workbench v4.1

A browser-side exploration tool for three synthetic healthcare datasets. It uses local CSV files shipped with the academy; it does not upload data or call external APIs.

## Capabilities
- Dataset selection and row-level filtering
- KPI calculation with explicit metric definitions
- Group-by summaries and category comparisons
- Data-quality checks for keys, missingness, chronology and implausible values
- CSV export of filtered rows and grouped summaries
- Chart interpretation prompts and a metric-contract reminder

## Privacy and limitations
All data are fabricated. The workbench runs calculations in the browser and stores only the user's checklist/progress locally. It is not a validated clinical system. It does not infer causality, medication adherence, adverse-event incidence or patient-level risk. It does not execute Python, SQL, DAX or Power Query.
