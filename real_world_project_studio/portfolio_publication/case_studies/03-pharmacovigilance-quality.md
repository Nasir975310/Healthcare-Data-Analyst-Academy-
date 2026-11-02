# Case study 03 — Pharmacovigilance case-quality review

## Business question
What data-quality checks and manual review workload should be surfaced for a synthetic adverse-event case register?

## Dataset and grain
240 fabricated case records, intended as one row per case record.

## Results from the reference run
- 240 case records.
- No missing or duplicate case IDs in the supplied fixture.
- No event-after-receipt chronology exceptions.
- Three records are flagged as duplicate candidates for manual review.

## Interpretation
Duplicate-candidate flags are review leads, not confirmed duplicates. Case counts by suspect drug are not incidence rates or comparative risks. Seriousness and severity are different concepts.

## Limitations
Synthetic data; no validated ICSR process; no licensed MedDRA coding; no expectedness, causality, signal detection or regulatory submission assessment.

## Reproduction
From `real_world_project_studio/`: `python scripts/run_all.py`, then `python portfolio_publication/scripts_dashboard_build.py`.
