# Healthcare data analyst interview question bank

Use a 60–120 second response per question. Strong answers define the metric, state the denominator/grain, explain validation, then connect the result to a bounded operational decision.

## SQL and data handling
1. **How would you find duplicate encounters?** Define the business key first; inspect duplicate groups; distinguish true repeat visits from duplicate ingestion; preserve an audit trail before deduplication.
2. **What is the difference between `COUNT(*)` and `COUNT(wait_minutes)`?** The former counts rows; the latter counts non-null wait values. Denominators must match the metric contract.
3. **How would you calculate department-level average wait?** Filter to eligible completed encounters, exclude invalid/missing wait values under an explicit rule, group by department, report both valid n and mean.
4. **How do you prevent join fan-out?** Check key uniqueness and row counts before/after joins; aggregate the many-side to the intended grain or use validated keys.
5. **When would you use a window function?** For within-group ranking, running totals or row-level comparisons without collapsing encounter grain.

## Statistics and interpretation
6. **Why report median as well as mean?** Wait times may be skewed; median is robust to long waits. Add percentiles and distribution plots when sample size permits.
7. **Does a higher mean prove a department is inefficient?** No. Case mix, time of day, appointment type, sample size and measurement validity may differ; the data are descriptive, not causal.
8. **How would you compare two departments?** First assess definitions, missingness, distribution and sample sizes; choose an appropriate inferential method only if the design and assumptions justify it; report effect size and uncertainty.
9. **How do you handle missing data?** Quantify and profile missingness; determine whether it is structural or process-related; do not impute zero by default; document denominator impact.

## Healthcare context, privacy and governance
10. **What is the difference between operational and clinical data?** Operational data describe processes such as appointments and waits; clinical data describe care, diagnoses and outcomes. They have different definitions, risks and validation requirements.
11. **How would you protect patient data?** Apply minimum-necessary access, approved environments, role-based permissions, secure transfer, retention controls and de-identification/pseudonymization where appropriate; follow organizational policy and applicable law.
12. **Can this synthetic project support a staffing change?** No. It demonstrates workflow only. A real decision requires validated source data, representative time periods, context, stakeholder review and monitoring.

## Communication and delivery
13. **A manager says your dashboard is wrong. What do you do?** Clarify the disputed metric and decision; reproduce the number from source rows; inspect filters, refresh, joins and definitions; communicate impact and correct transparently.
14. **How do you prioritize an urgent request?** Clarify decision deadline and risk; define minimum viable answer; validate critical fields; communicate caveats; schedule deeper analysis.
15. **Describe a mistake you found.** Use a real example from your own work only. Explain detection, root cause, correction, test added and prevention. Do not invent experience.

## Answer quality rubric
- 0: incorrect, unsupported or unsafe
- 1: partially correct but vague; no denominator or validation
- 2: technically sound with relevant caveat
- 3: technically sound, reproducible, stakeholder-oriented and explicit about limitations
