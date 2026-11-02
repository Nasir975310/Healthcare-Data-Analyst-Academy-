# Interactive Healthcare Analytics Workbench — v5.2.0

Open **Interactive analytics workbench v5.2** in the Academy navigation.

## Browser features
- Upload a local CSV or load the included synthetic sample.
- Inspect row/column counts, missing values, distinct counts, duplicate keys and heuristic numeric summaries.
- Preview cleaning with exact duplicate removal, duplicate-key exclusion and optional required-field rules.
- Export a cleaned CSV and a JSON profile report.
- Calculate a user-defined numerator/denominator KPI.
- Calculate mean, median and sample standard deviation for detected numeric columns.
- Copy SQL query templates for use in DBeaver/SQLite.
- Review a dashboard quality checklist.

CSV profiling, preview cleaning, KPI arithmetic and descriptive statistics are computed in the browser tab. This module does not transmit the CSV to a server. It does not execute SQL, Python, R, DAX or Power Query. SQL templates must be run separately in a database client.

## Python reference profile
From the Academy root:

```bash
python -m pip install pandas
python interactive_workbench_v52/scripts/profile_sample.py
```

Windows PowerShell:
```powershell
py -m pip install pandas
py interactive_workbench_v52/scripts/profile_sample.py
```

Outputs are created in `interactive_workbench_v52/output/`.

All bundled records are synthetic. Never use identifiable or confidential data in an unapproved environment.
