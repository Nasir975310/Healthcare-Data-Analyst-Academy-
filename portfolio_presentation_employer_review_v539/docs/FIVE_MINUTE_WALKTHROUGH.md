# Five-minute project walkthrough

Use this as a speaking outline, not a script to read verbatim.

## 0:00–0:40 — Problem and audience
"I built a synthetic outpatient operations analytics workflow to demonstrate how I would turn operational encounter records into validated, explainable summaries. It is an educational portfolio project, not a real hospital evaluation."

## 0:40–1:20 — Data and grain
Explain the encounter-level grain, the key identifier, source fields, synthetic provenance and why duplicate encounters matter. State the raw row count and curated count only after confirming them in your own latest run.

## 1:20–2:15 — Quality controls
Show the validation rules, duplicate handling, invalid wait-time checks, orphan handling if present, and exception output. Explain why rejected rows are retained for review rather than silently discarded.

## 2:15–3:15 — Metric logic
Choose one department-level metric. State:
- numerator or aggregation population;
- denominator / valid n;
- exclusions and missing values;
- unit and aggregation method;
- why the metric does not establish clinical quality or causality.

## 3:15–4:15 — Technical implementation
Walk through the pipeline, SQLite outputs, SQL query, tests and generated manifest. Explain how a reviewer can reproduce the result.

## 4:15–5:00 — Limitations and next step
Mention synthetic data, small sample, no inference about real hospital performance, no production integration, and what you would validate with stakeholders before operational use.

## Questions to prepare for
1. What is the grain of each table?
2. How do you prevent a join from inflating counts?
3. Why is valid wait-time n different from completed encounters?
4. How do you handle duplicate keys and missing values?
5. Which outputs are deterministic, and how do you know?
6. What would change before using this with real hospital data?
