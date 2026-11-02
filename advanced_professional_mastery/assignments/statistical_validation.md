# Statistical Validation Assignment — STAT-ADV-01

**Time:** 120 minutes · **Role:** Clinical / RWE Analyst

## Scenario
A synthetic observational cohort appears to show higher follow-up SBP among treated patients. Determine whether this crude comparison is robust to adjustment for baseline SBP, age and diabetes.

## Tasks
- Profile missingness and implausible ages.
- Define the complete-case analysis population and report all denominators.
- Estimate crude mean follow-up SBP by treatment status and the crude difference with 95% CI.
- Fit an adjusted linear model with robust (HC3) standard errors.
- Compare the crude and adjusted treatment coefficients and explain why direction can change.
- Discuss confounding by indication, unmeasured confounding, selection bias, model assumptions and missing-data handling.
- Do not call the adjusted coefficient a causal treatment effect.

## Data
`data/observational_sbp_cohort.csv` (1,200 synthetic rows).

## Reference
`solutions/statistical_validation.py` creates a JSON summary. Attempt the analysis before opening the reference output.
