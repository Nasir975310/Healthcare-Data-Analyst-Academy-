# Volume 4 project files

Run from this folder after installing pandas:

```bash
python -m pip install pandas
python analysis/analyze_cohort.py
```

Outputs are written to `outputs/`. The script validates required columns, unique synthetic patient identifiers and binary coding, then creates group summaries, missingness metrics and a validation log. The exercise is descriptive; it deliberately does not claim a causal treatment effect.
