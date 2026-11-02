# v5.49 dashboard QA

Run from this directory:

```bash
python -m unittest -v
python validate_dashboard.py
node test_reconciliation.js
```

The Python implementation is the independent reference. It emits `reconciliation.json` covering the unfiltered dataset, every drug class, each sex, all age bands, yes/no comorbidity filters, and combined filter permutations. Node recalculates those cases independently using JavaScript and checks every reported metric against the Python golden results. Dataset is synthetic.
