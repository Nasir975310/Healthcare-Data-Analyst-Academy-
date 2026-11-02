# ENG-02 — Antihypertensive drug-utilization evaluation

**Client:** Fictional clinical pharmacy committee  
**Decision:** What prescribing and blood-pressure patterns merit a chart-review follow-up?  
**Grain:** One row per synthetic patient.

## Request
Summarise prescribing status and antihypertensive class distribution. Describe baseline and follow-up systolic BP and paired change. Compare groups cautiously and identify missingness, eligibility and confounding concerns.

## Required deliverables
1. Cohort flow and data dictionary.
2. Prescribing and class distribution tables.
3. Paired SBP summary with N, mean change and uncertainty where appropriate.
4. Quality log and metric definitions.
5. A 300-word clinical-pharmacy interpretation that separates description from inference.

## Acceptance criteria
- Preserve the patient-level grain and unique patient key.
- Report missing baseline/follow-up counts and paired denominator.
- Define the direction of change (follow-up minus baseline).
- Do not equate prescription with dispensing, administration or adherence.
- Do not claim treatment efficacy or causality from this observational synthetic cohort.
- State that clinical thresholds/guidelines are not independently validated in this exercise.
