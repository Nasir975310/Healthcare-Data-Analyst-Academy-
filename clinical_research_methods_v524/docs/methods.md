# Methods and interpretation

## Nonparametric independent groups
Mann–Whitney U tests distributional/rank differences; it is not universally a test of medians. Cliff's delta estimates stochastic dominance and ranges from -1 to +1. Bootstrap confidence intervals resample independently within each group. Independence and sampling design remain essential.

## Paired and repeated measurements
Wilcoxon signed-rank uses paired differences and requires careful handling of zero differences and symmetry assumptions for a location-shift interpretation. The accompanying bootstrap interval targets mean change, not the Wilcoxon estimand. Friedman is a rank-based complete-case omnibus test for at least three related conditions; follow-up contrasts and multiplicity adjustment require a prespecified plan.

## Predictive validation
Stratified repeated K-fold CV creates out-of-fold predictions. The pipeline reports AUC, Brier score and calibration intercept/slope. Imputation and scaling are fit within each training fold via a pipeline. This reduces preprocessing leakage but does not replace nested CV for tuning, temporal validation or external validation. Very small samples and rare outcomes yield unstable metrics.

## Power planning
The power utility solves for group sample sizes for a two-sided independent-samples t-test under a standardized mean difference. It is not a substitute for design-specific power analysis, and attrition/design effects must be considered.

## Missingness
The report displays variable-level missingness and common missingness patterns. Descriptive patterns do not prove MCAR/MAR/MNAR. Mechanism assessment requires substantive knowledge and sensitivity analysis.

## Not implemented
Multiple imputation, clustered/paired bootstrap, GEE, mixed models, post-hoc repeated-measures contrasts, nested CV, external validation, decision-curve analysis and clinical decision support.
