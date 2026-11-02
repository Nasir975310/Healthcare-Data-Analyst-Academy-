# Interactive Healthcare Analytics Workbench — v5.2

## What runs in the browser
- CSV parsing and profiling are performed locally in your browser tab.
- Missing-value counts, duplicate-key checks, numeric summaries, preview and basic cleaning preview are calculated from the uploaded file.
- KPI arithmetic and descriptive statistics run client-side.
- Cleaned CSV and QA report can be exported.
- The SQL section generates query templates; it does **not** execute SQL. Use DBeaver/SQLite for execution.
- No file is uploaded to a server by this module. Do not use patient-identifiable or confidential data regardless.

## Start with the included sample
Open `data/workbench_sample.csv`, or use the CSV upload control in the workbench.

## Cleaning policy
The preview supports removal of exact duplicate rows and optional exclusion of rows missing selected required fields. It does not infer values, silently overwrite the source, or make clinical validity decisions. Export only after reviewing the exclusion count and rule.

## Statistical interpretation
Mean, median and sample standard deviation are descriptive. The browser module does not run inferential tests, adjust for confounding, establish causality or validate clinical measures. Check units, grain, distribution, missingness and denominator before interpreting.

## Privacy and production use
All bundled data are synthetic. Browser-side processing reduces transfer risk but does not make identifiable data safe to use in an unapproved environment. Follow institutional governance and de-identification requirements.
