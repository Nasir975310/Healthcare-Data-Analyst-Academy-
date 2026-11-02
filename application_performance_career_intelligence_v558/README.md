# Application Performance & Career Intelligence — v5.58

A local, dependency-free tracker analytics utility. It validates an application CSV, computes clearly defined pipeline metrics, and generates a standalone HTML dashboard plus JSON summary.

## Run on Ryoku / Linux

```bash
cd application_performance_career_intelligence_v558
python -m unittest discover -s tests -v
python src/application_metrics.py examples/demo_tracker.csv --out demo_output
```

Open `demo_output/dashboard.html` in a browser. The demo rows and organisations are fictional.

## Use your own applications

1. Copy `templates/application_tracker.csv` to a private working folder.
2. Add one row per vacancy/application. Use a unique `application_id`.
3. Keep `stage` to: `saved`, `applied`, `screening`, `assessment`, `interview`, `offer`, `rejected`, `withdrawn`.
4. Use `YYYY-MM-DD` for `applied_date`.
5. Run the command against your private tracker.
6. Keep the tracker local and exclude it from public Git repositories unless all employer/contact data has been removed.

## Metric definitions

- Submitted = all stages except `saved`.
- Response-stage proxy = stages `screening`, `assessment`, `interview`, `offer`, `rejected`, `withdrawn`, divided by submitted applications. Because this is a current-stage snapshot, it is not a true response-time metric.
- Interview rate = `interview` or `offer` divided by submitted applications.
- Offer rate = `offer` divided by submitted applications.
- CV comparison is descriptive only. Role mix, dates, sources and candidate differences are uncontrolled.

Empty denominators return null (displayed as a dash), not zero. The report does not calculate a hiring probability, causal CV effect, or time-to-response.
