-- 1. Records by primary drug class
SELECT primary_drug_class, COUNT(*) AS records FROM hypertension_records
WHERE primary_drug_class IS NOT NULL GROUP BY primary_drug_class ORDER BY records DESC;

-- 2. Mean baseline and follow-up SBP by primary drug class (complete plausible pairs only)
SELECT primary_drug_class, COUNT(*) AS paired_n,
 ROUND(AVG(baseline_sbp_mmhg),1) AS mean_baseline_sbp,
 ROUND(AVG(followup_sbp_mmhg),1) AS mean_followup_sbp,
 ROUND(AVG(baseline_sbp_mmhg-followup_sbp_mmhg),1) AS mean_change_sbp
FROM hypertension_records WHERE primary_drug_class IS NOT NULL
 AND baseline_sbp_mmhg BETWEEN 70 AND 250 AND followup_sbp_mmhg BETWEEN 70 AND 250
GROUP BY primary_drug_class ORDER BY paired_n DESC;

-- 3. Regimen complexity and adherence distribution
SELECT antihypertensive_count, adherence_category, COUNT(*) AS n
FROM hypertension_records GROUP BY antihypertensive_count, adherence_category
ORDER BY antihypertensive_count, adherence_category;

-- 4. Comorbidity profile
SELECT diabetes, ckd, ischemic_heart_disease, COUNT(*) AS n
FROM hypertension_records GROUP BY diabetes, ckd, ischemic_heart_disease;
