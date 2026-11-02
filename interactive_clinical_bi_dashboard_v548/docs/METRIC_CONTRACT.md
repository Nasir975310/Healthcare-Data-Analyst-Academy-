# Dashboard metric contract

| Metric | Definition | Denominator |
|---|---|---|
| Filtered records | Raw rows matching current filters | All matching raw rows |
| Unique record IDs | Distinct `record_id` among matching rows | All matching raw rows |
| Paired SBP records | Valid primary class + plausible baseline and follow-up SBP (70–250 mmHg) | Matching rows eligible for paired analysis |
| Mean baseline SBP | Arithmetic mean baseline SBP | Paired SBP records |
| Mean follow-up SBP | Arithmetic mean follow-up SBP | Paired SBP records |
| Mean paired change | Mean of baseline SBP − follow-up SBP | Paired SBP records |
| Duplicate excess | Filtered rows minus unique IDs | Filtered raw rows |
| Missing follow-up | Blank follow-up SBP | Filtered raw rows |
| Implausible follow-up | Nonblank follow-up SBP outside 70–250 | Filtered raw rows |
| At least one comorbidity | Any of `diabetes`, `ckd`, `ischemic_heart_disease` is positive | Rows with a known positive indicator |
| No recorded comorbidity | All three indicators are explicitly negative | Rows with all three indicators known |

Comorbidity classification is tri-state: a positive indicator means `yes`; all three explicit negatives mean `no`; otherwise it is unknown and excluded from both yes/no filters. The literal string `None` is treated as a missing primary drug class, not a valid class.
