# Interactive Clinical BI Dashboard — v5.48

## Launch
From the Academy root:
```bash
cd interactive_clinical_bi_dashboard_v548
python -m http.server 8000
```
Open `http://localhost:8000/dashboard/` in a browser. The dashboard loads `data/dashboard_data.json` using `fetch`, so it must be served over HTTP; opening the HTML directly with `file://` will not load the data file in many browsers.

## Features
- Filter by primary drug class, sex, age band and recorded comorbidity.
- KPI cards update with filters.
- Class-level paired SBP change chart and follow-up SBP histogram.
- Dynamic class summary and data-quality indicators.
- Export filtered source rows to CSV.
- Responsive layout and keyboard-focus styles.

## Metric contract
- Record-level filtering is applied before calculations.
- Paired SBP requires known primary drug class and both SBP values in [70, 250].
- SBP change = baseline − follow-up.
- The dashboard displays all raw rows under the filters; duplicate excess and unique IDs are shown separately.
- Class summaries use eligible paired records and show n.

## Limitations
All records are synthetic. No causal inference or prescribing recommendation. This is a browser-based interactive dashboard, not a Power BI `.pbix` file. It is a Linux-compatible local dashboard deliverable; no external service is required.
