# v5.47 Reporting Pack

This module turns the v5.46 synthetic medication-utilization project into a stakeholder-facing report, reproducible figures, statistical-methods note, Power BI model specification, DAX measures and presentation/defense materials.

## Run
From the Academy root:
```bash
python clinical_analytics_reporting_pack_v547/src/build_report.py
```
Requires Python, pandas, NumPy, SciPy and Matplotlib. The HTML report and figures are generated under this module's `outputs/`. The current included report was generated from the included synthetic CSV.

## Important
No `.pbix` dashboard was created or executed. `powerbi/` contains a model specification and DAX measures for implementation in Power BI Desktop. This pack is not clinical evidence and does not use the user's Pharm.D thesis dataset.
