# ENG-03 — Pharmacovigilance case-quality review

**Client:** Fictional drug-safety operations lead  
**Decision:** Which records need manual data-quality review before downstream processing?  
**Grain:** One row per safety case.

## Request
Profile the case register, review chronology, missingness, serious flag distribution and duplicate-candidate flags. Produce a review queue without making causality or signal conclusions.

## Required deliverables
1. Case-level quality profile.
2. Duplicate-candidate review queue.
3. Chronology exception report.
4. Seriousness/outcome descriptive summary with clear denominators.
5. Reviewer handoff note and limitations.

## Acceptance criteria
- Preserve all source case IDs and duplicate candidates.
- Check event-onset/report-received chronology and missing values.
- Do not infer causality, expectedness, signal, incidence or regulatory reportability.
- Distinguish seriousness from severity.
- Use only synthetic records and document manual review status.
