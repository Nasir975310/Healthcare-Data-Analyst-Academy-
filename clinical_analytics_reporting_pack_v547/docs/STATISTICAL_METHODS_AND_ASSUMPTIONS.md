# Statistical methods and assumptions

## Population and estimand
The analysis uses unique synthetic records with a known primary drug class and baseline SBP in the pre-specified screening interval 70–250 mmHg. Paired SBP summaries additionally require follow-up SBP in that interval. The descriptive estimand is the mean within-record baseline-minus-follow-up SBP difference among complete eligible pairs.

## Results from this generated dataset
- Paired records: 296
- Mean paired SBP change: 13.24 mmHg
- SD: 10.20 mmHg
- 95% t-based CI: 12.07 to 14.40 mmHg
- One-sample t-test against zero: t=22.333, p=2.2952e-65
- Wilcoxon signed-rank test: statistic=1587.5, p=3.5415e-43
- Unadjusted one-way ANOVA across classes: F=1.819, p=0.12507

## Assumptions and caveats
- Paired t-test: independent records, approximately normal distribution of within-record differences (or sufficiently robust sample size), and no extreme influential observations.
- Wilcoxon signed-rank: paired differences are independent and approximately symmetric for a location-shift interpretation.
- One-way ANOVA: independent observations, approximately normal residuals within groups and homogeneity of variance. Inspect residuals and variance diagnostics before relying on it.
- Confidence intervals are unadjusted and do not address confounding, missing-data mechanisms or multiple comparisons.
- Class-level differences are not causal or comparative effectiveness estimates. No dose, duration, titration, co-interventions or adequate confounder adjustment are included.
- Statistical significance is not equivalent to clinical importance.

## Better real-world design
For real clinical data, pre-specify the target population, time window, outcome, missing-data plan and confounder set. Consider multivariable regression or propensity methods only when justified by the causal question, overlap and data quality. Obtain appropriate approvals and de-identify data before analysis.
