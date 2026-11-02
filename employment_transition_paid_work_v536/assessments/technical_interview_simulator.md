# Technical interview simulator

Answer aloud in 90–150 seconds each. Score each answer 0–4: 0 incorrect/unsafe; 1 vague; 2 partly correct; 3 correct and structured; 4 correct, quantified where appropriate, and limitations-aware.

1. What is the grain of an encounter fact table? How do you prove it?
2. Explain the difference between `COUNT(*)`, `COUNT(column)` and `COUNT(DISTINCT patient_id)`.
3. A join doubles medication orders. How do you diagnose fan-out?
4. How do you handle duplicate source records without deleting legitimate repeat visits?
5. Define a denominator for median wait time.
6. What is the difference between missing, zero and not applicable?
7. How would you reconcile source and curated row counts?
8. What belongs in a data dictionary and metric contract?
9. How do you explain an unexpected KPI change to a nontechnical manager?
10. Why can an observational association not establish causation?
11. What steps protect patient confidentiality in a portfolio?
12. What do you do when the requested metric cannot be calculated reliably?

## Answer structure
Clarify the business question → state grain/cohort → describe method → name validation → communicate result → state limitation/escalation. Never invent a result when the data is insufficient.
