# Healthcare BI Portfolio & Client Reporting — v5.29.0

This cumulative module extends v5.28. It adds a portfolio case study, standard-library Python reporting pipeline, SQL reconciliation queries, QA outputs, dashboard specification and client handover checklist.

## Quick start
From this module directory:

```bash
python src/build_portfolio.py
python -m unittest discover -s tests -v
```

All inputs are synthetic and copied from the v5.28 training dataset. Outputs are written to `reports/`. Python generation and tests execute locally. Power Query and DAX remain templates requiring Power BI Desktop validation.
