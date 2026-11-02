# Clinical Research Methods Engine v5.24.0

A local Python workflow adding nonparametric effect sizes, paired and repeated-measures methods, cross-validated prediction, power planning and descriptive missingness assessment.

## Run

From the Academy root:

```bash
python -m pip install -r clinical_research_methods_v524/requirements.txt
python clinical_research_methods_v524/scripts/clinical_methods.py \
  --input clinical_research_methods_v524/data/synthetic_clinical_methods.csv \
  --config clinical_research_methods_v524/templates/clinical_methods_config.json \
  --output clinical_research_methods_v524/outputs/demo
```

## Included methods
- Mann–Whitney U with Cliff's delta and bootstrap interval for the effect size.
- Paired Wilcoxon signed-rank test, with a separately labelled bootstrap CI for arithmetic mean change.
- Friedman repeated-measures test with Kendall's W.
- Stratified repeated cross-validation for logistic prediction, pooled out-of-fold ROC AUC, Brier score and calibration intercept/slope.
- Two-independent-group mean-comparison power/sample-size calculation.
- Descriptive missingness pattern summaries.

## Statistical boundaries
The Mann–Whitney p-value and Cliff's delta are distinct inferential summaries. The paired Wilcoxon test and mean-change bootstrap interval target different estimands. Friedman is complete-case and does not include post-hoc contrasts. CV performance is internal validation, not external validation; nested CV and fold-level uncertainty are not implemented. Calibration estimates are derived from out-of-fold predictions on the same dataset. Power calculation is a two-sample independent-means approximation. Missingness patterns alone cannot identify MCAR, MAR or MNAR. No multiple imputation is included; median imputation is used only inside predictive CV folds. All examples use synthetic data.
