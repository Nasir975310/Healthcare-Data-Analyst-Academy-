# Interview Preparation

## Five-minute portfolio walkthrough

1. **Problem:** The project demonstrates how data-quality exclusions affect outpatient waiting-time summaries.
2. **Data:** 24 fictional encounter rows; no real patient information.
3. **Quality:** One duplicate, one negative wait and one missing department are handled under documented rules.
4. **Metrics:** Explain completed encounters and valid waiting-time denominators.
5. **Findings:** Present department means with sample sizes; avoid causal interpretation.
6. **Reproducibility:** Run the Python pipeline, tests and preflight.
7. **Limitations:** Small synthetic dataset; not generalizable and not a clinical/operational decision tool.

## Questions to prepare

### Healthcare and clinical data
- How do you protect patient confidentiality?
- What is the difference between a clinical variable and an operational metric?
- How would you handle conflicting values in a patient record?
- Why should missing values not be replaced with zero automatically?
- What is the difference between prospective and retrospective observational designs?

### SQL and analytics
- Explain INNER JOIN versus LEFT JOIN.
- How would you identify duplicate encounter IDs?
- How do WHERE and HAVING differ?
- How do you calculate a department-level average with a valid denominator?
- How do you handle NULL values in aggregate functions?
- What is the difference between COUNT(*) and COUNT(column)?
- How would you validate a dashboard total against its source query?

### Statistics and interpretation
- What does a confidence interval communicate?
- When might a paired t-test be appropriate?
- What assumptions matter for one-way ANOVA?
- Why is a statistically significant result not necessarily clinically important?
- Why do unadjusted group comparisons not establish causality?

### Behavioral
- Describe a time you found a data-quality issue.
- How would you explain a limitation to a nontechnical stakeholder?
- What would you do if a manager asked you to remove inconvenient records without a documented rule?
- How do you prioritize accuracy when deadlines are tight?

## Honest response when asked about experience

Use a clear distinction: academic clinical research experience, synthetic portfolio project experience and professional employment experience are not interchangeable. Describe the work you personally performed and state when a project used fictional data.
