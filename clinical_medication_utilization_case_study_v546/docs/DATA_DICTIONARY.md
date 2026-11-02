# Data dictionary

| Field | Type | Meaning |
|---|---|---|
| record_id | string | Synthetic unique encounter/record key |
| age_years | integer | Age in years |
| sex | category | Female or Male (synthetic field) |
| diabetes, ckd, ischemic_heart_disease | 0/1 | Simulated comorbidity indicators |
| primary_drug_class | category | One primary antihypertensive class |
| regimen_classes | string | Simulated regimen class labels |
| antihypertensive_count | integer | Number of agents represented |
| adherence_category | category | Simulated High/Moderate/Low category |
| baseline_sbp_mmhg / baseline_dbp_mmhg | numeric | Simulated baseline BP |
| followup_sbp_mmhg / followup_dbp_mmhg | numeric | Simulated follow-up BP; may be missing |
| followup_days | integer | Simulated follow-up interval |

Grain: one synthetic record per record ID. The source intentionally contains one duplicate row. No direct identifiers exist.
