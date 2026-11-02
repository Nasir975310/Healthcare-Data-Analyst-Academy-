# Power BI model specification

## Purpose
A descriptive monitoring view for the fictional synthetic antihypertensive dataset. This is a build specification; no `.pbix` file is included or claimed.

## Import
Load `clinical_medication_utilization_case_study_v546/data/synthetic_hypertension_records.csv` as `FactHypertension`. Keep `record_id` as a text key. Do not silently drop invalid rows in Power Query; retain quality flags and document the analysis population.

## Suggested Power Query steps
1. Set `record_id` and category columns to Text; clinical measurements to Decimal Number; comorbidity indicators and medication count to Whole Number.
2. Create `IsDuplicate` using grouped `record_id` counts.
3. Create `IsValidBaselineSBP` for 70–250 mmHg.
4. Create `IsValidFollowupSBP` for nonblank follow-up SBP in 70–250 mmHg.
5. Create `IsKnownPrimaryClass` for nonblank primary drug class.
6. Create `IsPairedSBPEligible` as valid baseline AND valid follow-up AND known class AND nonduplicate.
7. Retain the raw table for quality monitoring; use a filtered analysis table or measures for eligible rows.

## Report pages
- Overview: raw rows, unique IDs, eligible paired rows, missing/invalid follow-up count.
- Utilization: primary class distribution, regimen complexity and adherence categories.
- BP follow-up: baseline/follow-up mean and paired SBP change by class, with n shown.
- Data quality: duplicates, missing class, missing BP, implausible BP.
- Definitions: metric contract, synthetic-data warning and limitations.

## Visual design
Use accessible contrast, descriptive titles, visible denominators, units, filter context and tooltips. Avoid red/green-only status encoding. Display sample size beside every class-level statistic. Do not rank drug classes as more effective.

## Validation
Reconcile card totals against Python `analysis_results.json`. Test slicers for class, age band, sex and comorbidity; ensure denominators update consistently. Do not mix raw-row counts with eligible paired denominators.
