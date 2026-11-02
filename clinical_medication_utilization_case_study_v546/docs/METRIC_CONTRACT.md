# Metric contract

| Metric | Definition | Denominator / caveat |
|---|---|---|
| Raw rows | Number of CSV rows | Includes intentional duplicate |
| Unique IDs | Distinct record_id values | Duplicate IDs collapse to one |
| Clean rows | Unique records with known primary drug class and valid baseline SBP | Excludes missing/unknown class or invalid baseline |
| Paired SBP rows | Clean rows with plausible follow-up SBP | Complete-pair subset; missingness may bias summaries |
| Mean SBP change | Mean(baseline SBP - follow-up SBP) | Positive value indicates lower follow-up SBP in this synthetic paired subset; descriptive only |
| Illustrative BP below 140/90 | Follow-up SBP <140 AND DBP <90 | Educational convention, not individualized target |

No inferential tests or causal effects are claimed. Class-level means are not adjusted for case mix, dose, duration, co-interventions or baseline severity.
