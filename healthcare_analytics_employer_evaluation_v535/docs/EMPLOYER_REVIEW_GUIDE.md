# Employer review guide

## Inspectable evidence
1. Business question and KPI definitions.
2. Raw-to-curated pipeline, data dictionary, lineage and exception handling.
3. Rerunnable SQL and Python.
4. Independent reconciliation between analysis and dashboard.
5. Synthetic/licensed inputs and no credentials.
6. Findings with denominators, dates and limitations.
7. Clean-checkout reproduction instructions.

## Five-minute portfolio tour
- 0:00–0:45 — business problem, users and scope.
- 0:45–1:30 — source files, grain and data-quality risks.
- 1:30–2:30 — pipeline, curated warehouse and rejected orphan.
- 2:30–3:30 — KPI query and dashboard; reconcile one metric live.
- 3:30–4:15 — privacy, security and limitations.
- 4:15–5:00 — next improvements and remaining external evidence.

## Likely reviewer questions
- Why preserve an invalid row instead of deleting it?
- What is the grain of each fact table?
- Why is medication order count not adherence?
- How did you prove the dashboard denominator?
- What happens when a file is ingested twice?
- How would you prevent a many-to-many relationship?
- What would you monitor after deployment?
- Which parts did you personally execute, and in which environment?

Never describe synthetic work as a real client engagement. Label dashboard specifications as specifications, not implemented dashboards.
