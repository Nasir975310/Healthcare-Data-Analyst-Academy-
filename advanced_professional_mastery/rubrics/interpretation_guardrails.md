# Interpretation guardrails

1. A supplied binary readmission-like flag is not automatically a validated readmission outcome.
2. Medication order records do not establish dispensing, administration, ingestion or adherence.
3. A one-to-many join can multiply encounter-level measures. Aggregate at the intended grain first.
4. A regression-adjusted association is not automatically a causal effect.
5. Report complete-case denominators and missingness; do not imply missing-at-random without evidence.
6. Confidence intervals quantify model-based uncertainty, not all sources of bias.
7. Synthetic data are useful for skill practice but cannot support clinical or operational conclusions about a real institution.
