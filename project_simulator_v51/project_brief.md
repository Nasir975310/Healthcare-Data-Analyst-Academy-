# Client engagement: monthly hospital flow and data-quality review

## Initial request
The Operations Manager asks for a monthly report showing encounter volume by department, average length of stay (LOS), disposition mix, and systolic blood pressure (SBP) completeness. They want a one-page summary and a reproducible data pack.

## Data contract (initial)
- Grain: one row per encounter.
- Reporting period: 1 January–1 March 2026, inclusive.
- Encounter identifier: `encounter_id` (expected unique).
- LOS: discharge date minus admission date, in calendar days.
- SBP completeness: percentage of accepted encounters with a recorded, valid SBP.
- All records are synthetic training data.

## Client messages arrive during the engagement
1. **Scope clarification:** exclude Emergency from the department comparison, but retain it in the overall hospital total.
2. **Metric change:** calculate average LOS using discharged encounters only; show transferred and admitted encounters in the disposition mix.
3. **Quality escalation:** do not silently repair missing department or patient identifiers. Quarantine records with invalid keys, dates, or SBP values; preserve the reason codes.
4. **Handoff request:** provide a reproducible script, SQL summary, quality log, limitations and a concise client note.

## Required outputs
- Raw-to-accepted/quarantined reconciliation.
- Department summary excluding Emergency, plus separate overall total.
- Disposition mix.
- Discharged-only average LOS.
- SBP completeness among accepted records.
- QA log and client-facing caveats.

## Decision boundaries
Do not infer clinical quality from SBP completeness or utilization counts. No treatment-effect or causal claims. This is an operational analytics exercise, not clinical decision support.
