# Healthcare statistical visualization methodology

## Figure selection
- **Histogram / density:** inspect a continuous variable's shape, skew and possible outliers. Bin width changes appearance; show sample size and units in final publication.
- **Box plot:** compare median, quartiles and potential outliers across groups. Box plots conceal multimodality and small-sample detail; consider jittered points or violin plots as supplements.
- **Forest plot:** display study-level effect estimates and confidence intervals on a logarithmic axis for ratio measures. The vertical reference is 1 for ratios. This module does not pool estimates or calculate heterogeneity.
- **ROC curve:** show sensitivity against 1 − specificity across thresholds using patient-level reference outcomes and scores. Apparent AUC is optimistic when assessed on training data; use held-out or resampling validation for model performance claims.
- **Kaplan–Meier:** estimate the product-limit survival function. Censoring is assumed non-informative for standard interpretation. Report numbers at risk and confidence intervals in a publication; this educational module currently plots curves only.

## Publication checklist
1. Give every axis a meaningful label and unit; avoid unexplained abbreviations.
2. Report analysis n, missingness and exclusions.
3. Identify the study design, time origin, endpoint and censoring definition.
4. Use a scale appropriate to the estimand; ratio measures often require a log axis.
5. Avoid truncated axes that exaggerate differences.
6. Distinguish descriptive plots from inferential analyses.
7. Do not use colour as the only means of distinguishing groups; consider accessible line styles and labels.
8. State whether ROC performance is apparent, internally validated or externally validated.
9. For survival figures, include censoring marks, confidence bands and numbers-at-risk in final research outputs where appropriate.
10. Preserve the source data, analysis script, package versions and figure-generation parameters.

## Meta-analysis boundary
A forest plot can display externally calculated estimates and confidence intervals. It is not a meta-analysis engine. Pooling requires a prespecified effect measure, model (fixed/common vs random effects), within-study variance, between-study variance estimator, heterogeneity assessment and sensitivity analyses. Do not infer a pooled effect from the visual midpoint or an arithmetic average of study estimates.

## Data integrity
The script records the input SHA-256 in the report. This supports lineage, but does not prove source authenticity, correctness, or absence of manipulation. The included example data are synthetic.
