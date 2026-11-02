# ENG-01 — Hospital operations performance review

**Client:** Fictional tertiary hospital operations team  
**Decision:** Which departments require an operational deep dive next month?  
**Deadline:** 4 working hours  
**Grain:** One row per encounter in `hospital_encounters_raw.csv`.

## Request
Produce a department-level performance pack from the supplied synthetic encounter file. Review encounter volume, mean and median length of stay, age distribution, and supplied readmission flag rate. Identify data limitations and avoid interpreting the supplied flag as a validated 30-day readmission outcome.

## Required deliverables
1. Data profile and quality log.
2. Department KPI table with explicit numerator/denominator and time period.
3. One decision-focused dashboard or equivalent visual.
4. Executive summary (maximum 300 words) with three findings, two limitations and two recommended investigations.
5. Reproducibility instructions and a handoff checklist.

## Acceptance criteria
- Reconcile total rows and unique encounter IDs.
- Validate date order and plausible LOS; preserve and document exceptions.
- Report mean and median LOS, not mean alone.
- Show department denominators; do not rank tiny groups without context.
- Explain that a supplied flag is not a validated readmission definition.
- Include source file hash and software/run instructions.

## Reviewer prompts
Can a reviewer rerun the analysis? Is the grain clear? Do totals reconcile? Are recommendations supported by the data?
