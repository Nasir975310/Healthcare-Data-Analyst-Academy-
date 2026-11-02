# Case study 01 — Hospital operations performance pack

## Business question
How does encounter volume and length of stay vary by department, and what data-quality caveats must accompany the management view?

## Dataset and grain
1,200 fabricated encounter records; one row is intended to represent one encounter. There are 611 distinct synthetic patients. The encounter and patient counts are not interchangeable.

## Method
- Profile keys, missingness and chronology.
- Validate encounter uniqueness and discharge/admission chronology.
- Calculate department encounter counts and mean length of stay.
- Label the supplied flag as unvalidated rather than asserting a readmission rate.

## Results from the reference run
- 1,200 source rows; 1,200 retained after the documented basic checks.
- 611 distinct synthetic patients.
- Overall mean length of stay: 5.27 days.
- Supplied flag proportion: 9.50%, explicitly unvalidated.

## Interpretation
This is a descriptive operational snapshot. Mean LOS may reflect case mix, service-line practice, discharge pathways and data capture. It is not a standalone quality ranking.

## Limitations
Synthetic data; no case-mix adjustment; supplied flag not validated; no staffing, bed capacity, severity or cost context.

## Reproduction
From `real_world_project_studio/`: `python scripts/run_all.py`, then `python portfolio_publication/scripts_dashboard_build.py`.
