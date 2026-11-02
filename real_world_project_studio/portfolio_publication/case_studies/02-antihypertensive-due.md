# Case study 02 — Antihypertensive drug-utilisation evaluation

## Clinical question
Describe recorded antihypertensive prescribing and systolic BP patterns in a synthetic observational cohort.

## Dataset and grain
500 fabricated patient-level cohort records with baseline/follow-up systolic BP and a binary recorded-prescribing indicator.

## Results from the reference run
- 500 complete, plausible records in this fixture.
- 158 records in the prescribed group and 342 in the no-prescription group.
- Mean baseline SBP: 159.33 mmHg (prescribed) and 158.79 mmHg (no prescription).
- Mean follow-up SBP: 150.57 mmHg (prescribed) and 154.43 mmHg (no prescription).
- Mean paired change: −8.76 mmHg and −4.37 mmHg, respectively.

## Interpretation
The observed group differences are descriptive. Treatment selection, confounding, measurement timing and unmeasured clinical factors prevent causal attribution. A prescription does not establish dispensing, administration, ingestion or adherence.

## Limitations
Synthetic data; no randomisation; no causal design; no validated BP measurement protocol; no external clinical review.

## Reproduction
From `real_world_project_studio/`: `python scripts/run_all.py`, then `python portfolio_publication/scripts_dashboard_build.py`.
