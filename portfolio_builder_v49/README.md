# v4.9.0 — Professional Project Portfolio Builder

Turn a completed analytics project into inspectable employer-facing evidence. This kit generates a factual project inventory, data dictionary, metric contract, QA summary and README draft from your v4.8 project outputs. It does not publish to GitHub or verify claims beyond the files and checks it reads.

## Run
From this directory, after the v4.8 project has been run:

```bash
python scripts/build_portfolio_pack.py --project ../project_execution_v48 --output output
python -m pytest -q
```

The generated pack is placed in `output/`. Review every statement and replace the draft case study with your own verified interpretation. Do not include real patient data, credentials, private paths or client information.

## Deliverables
- Project README draft
- Data dictionary
- Metric definition contract
- QA and reproducibility summary
- Portfolio evidence inventory
- CV bullet evidence worksheet
- Interview preparation prompts
- Publication checklist

All data in the included project is synthetic. No automatic GitHub publishing, job applications or external verification is performed.
