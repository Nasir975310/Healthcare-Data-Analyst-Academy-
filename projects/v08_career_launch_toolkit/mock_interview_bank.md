# Healthcare Data Analyst mock interview bank

Use these as practice prompts. Answer with a structured explanation and, where possible, a small worked example.

## SQL and data quality
1. Two tables contain patient and encounter records. How do you prevent row multiplication when joining them?
2. Explain the difference between COUNT(*), COUNT(column) and COUNT(DISTINCT patient_id).
3. How would you investigate a sudden 25% fall in monthly encounter volume?
4. How would you validate a medication table with repeated orders and cancelled prescriptions?

## Statistics and clinical context
5. Explain confidence interval versus p-value to a non-statistician.
6. Why can PPV change when prevalence changes even if sensitivity and specificity remain constant?
7. Describe confounding and why an association between a drug and an outcome is not automatically causal.
8. What checks would you perform before comparing two departments?

## Python and BI
9. Describe a reproducible pandas data-cleaning workflow.
10. How do you handle missing values without hiding the missingness pattern?
11. What makes a dashboard metric definition auditable?
12. How would you investigate a discrepancy between a dashboard and a SQL extract?

## Professional practice
13. Tell me about a time you found an error and how you handled it.
14. How do you clarify an ambiguous stakeholder request?
15. How do you work asynchronously across time zones?
16. What would you do if a client sent patient data to your personal email?

## Case exercise
A hospital manager asks for a dashboard showing medication utilisation by department. Clarify the metric, define the data grain, identify required tables, plan validation, state privacy safeguards, and propose a concise handoff. Do not assume that a prescription equals administration or consumption.
