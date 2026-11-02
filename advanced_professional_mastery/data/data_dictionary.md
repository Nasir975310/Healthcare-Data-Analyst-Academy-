# Data dictionary

| Table/file | Field | Meaning | Grain / unit |
|---|---|---|---|
| encounters | encounter_id | Unique synthetic encounter key | One row per encounter |
| encounters | patient_id | Synthetic patient key | Repeats across encounters |
| encounters | los_days | Length of stay | Days |
| encounters | readmit_30d_flag | Supplied synthetic flag | Binary; not validated |
| medication_orders | order_id | Unique synthetic order key | One row per medication order |
| medication_orders | encounter_id | Encounter reference | May be orphaned |
| medication_orders | quantity | Ordered quantity | Synthetic units; not dispensing |
| medication_orders | unit_cost | Simulated unit cost | INR; some missing |
| lab_observations | observation_id | Unique synthetic observation key | One row per observation |
| lab_observations | code | Observation type | SBP, DBP, creatinine, HbA1c |
| lab_observations | value | Numeric result | Interpret with unit field |
| observational_sbp_cohort | study_id | Synthetic cohort record key | One row per synthetic participant |
| observational_sbp_cohort | treated | Simulated treatment indicator | Binary |
| observational_sbp_cohort | baseline_sbp / followup_sbp | Simulated SBP | mmHg |
| observational_sbp_cohort | diabetes | Simulated covariate | Binary |

All identifiers are fictional. Values do not represent clinical practice, patient outcomes or actual hospital performance.
