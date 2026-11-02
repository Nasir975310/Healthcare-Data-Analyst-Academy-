# Workbench metric definitions

## Hospital operations
- Encounter count: number of rows after the selected filters. The shipped fixture is designed with one row per encounter; confirm uniqueness before using this as a count of distinct encounters.
- Unique patients: distinct patient IDs among filtered encounter rows.
- Mean length of stay: arithmetic mean of `length_of_stay_days` over nonmissing values.
- Supplied flag proportion: sum of the supplied binary flag divided by rows with a nonmissing flag. This is not a validated readmission rate.

## Antihypertensive DUE
- Cohort count: number of filtered records.
- Treated group: rows where `prescribed_any_antihypertensive = 1`.
- Mean SBP change: mean of follow-up SBP minus baseline SBP. Negative values indicate lower follow-up SBP.
- Class counts: rows by recorded class. A prescription is not proof of dispensing, administration, ingestion or adherence.

## Pharmacovigilance
- Case records: count of filtered case rows.
- Serious case proportion: rows with `serious_flag = 1` divided by rows with a nonmissing flag.
- Duplicate-candidate count: number of records with candidate flag 1. This is a manual-review queue, not a confirmed duplicate count.
- Case counts are not incidence rates or comparative risks.
