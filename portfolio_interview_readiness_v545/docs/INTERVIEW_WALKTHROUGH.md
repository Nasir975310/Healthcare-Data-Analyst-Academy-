# Five-minute portfolio walkthrough

## 0:00–0:40 — Business question
“I built a small outpatient operations analytics project to demonstrate how I would turn encounter-level operational data into quality-checked, decision-oriented reporting. The dataset is entirely synthetic.”

State the intended audience (clinic operations manager) and decision: where should a manager investigate waiting-time performance and data reliability first?

## 0:40–1:30 — Data and grain
Explain that one row represents one outpatient encounter. Describe the fields from `docs/data_dictionary.md`, the inclusion rules from `docs/metric_contract.md`, and the limitations: small synthetic sample, no patient identifiers, no causal inference, no clinical quality endpoint.

## 1:30–2:30 — Quality controls
Walk through duplicate handling, missing/invalid wait-time treatment, status eligibility and the distinction between excluded records and valid denominator records. Explain why missing values are not silently replaced with zero.

## 2:30–3:30 — Analysis and SQL
Show the SQL aggregation and Python pipeline. Explain count, mean wait time and department-level comparisons. Distinguish descriptive summaries from statistical inference; do not imply the small sample proves one department is worse.

## 3:30–4:20 — Findings and action
Use only the values in `docs/reference_results.md` and the generated output from a fresh run. Recommend validating timestamps and reviewing queue processes in a larger, real operational dataset before changing staffing or policy.

## 4:20–5:00 — Limitations and next iteration
Propose: validate source-system definitions; add arrival-to-triage and triage-to-provider timestamps; stratify by appointment type and hour; monitor median and 90th percentile; add a run chart with confidence/context; obtain privacy and stakeholder approval.

## Demonstration checklist
- [ ] Open README and explain one-row-per-encounter grain.
- [ ] Show the data dictionary and metric contract.
- [ ] Run the project from a clean environment.
- [ ] Show tests and generated outputs.
- [ ] Explain one excluded record and why it was excluded.
- [ ] State three limitations without prompting.
- [ ] Avoid causal, clinical or real-world claims unsupported by the data.
