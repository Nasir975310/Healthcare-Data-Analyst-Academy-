# Statistical analysis planning guide

## Before running a test
1. Identify the estimand, population, outcome, exposure/group, time point and unit of analysis.
2. Confirm study design, independence/paired structure, repeated measures and clustering.
3. Define primary and secondary outcomes, contrasts, alpha, confidence level and multiplicity strategy in advance.
4. Inspect variable types, missingness, distributions, outliers and data provenance.
5. Select a method based on design and estimand—not a normality-test p-value alone.

## Method map

| Question / data structure | Candidate method | Key checks |
|---|---|---|
| One continuous variable | Mean/SD, median/IQR, distribution plot | Skew, outliers, measurement scale |
| Two independent means | Welch t-test | Independence; residual/distribution behaviour |
| Two paired means | Paired t-test | Paired observations; distribution of differences |
| Two independent ordinal/skewed groups | Mann–Whitney U | Interpret as rank/distribution comparison |
| Categorical association | Chi-square; Fisher exact for sparse 2x2 | Expected cell counts, independent observations |
| Two continuous variables | Pearson or Spearman | Linearity / monotonicity, outliers |
| Continuous outcome with predictors | Linear regression / ANCOVA | Linearity, residuals, homoscedasticity, influence, confounding |
| Binary outcome | Logistic regression | Events per parameter, separation, calibration, confounding |
| Time-to-event outcome | Kaplan–Meier / Cox model | Censoring, proportional hazards, competing risks |

## Effect sizes and uncertainty
Report an interpretable effect estimate with a confidence interval (e.g., mean difference, risk ratio, odds ratio, correlation), not only a p-value. Define the contrast direction and clinical/practical threshold. A confidence interval describes uncertainty under model assumptions; it is not a probability statement about a fixed parameter.

## Missing data
Report missing n and percentage by variable and, where relevant, by group/time. Describe patterns and plausible mechanisms (MCAR, MAR, MNAR). Complete-case analysis can be biased; multiple imputation or weighting requires defensible assumptions and specialist review. Never silently replace missing values with zero.

## Multiple testing and subgroup analysis
Prespecify a primary endpoint. Label exploratory analyses. Consider family-wise error or false-discovery-rate control when many hypotheses are tested. Avoid post-hoc subgroup claims.

## Causal and clinical interpretation
Observational comparisons are vulnerable to confounding, selection bias and measurement error. Statistical significance is not clinical importance. The module's synthetic dataset is for training only; it is not evidence about hypertension treatment effectiveness.
