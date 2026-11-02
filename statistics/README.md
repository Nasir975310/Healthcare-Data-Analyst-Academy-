# Advanced Statistics and Clinical Research Laboratory

Dataset: `data/synthetic_clinical_cohort.csv` (400 fully synthetic records). The data are generated for training and do not represent real patients, clinical outcomes or treatment effects.

## Python setup
Create a virtual environment, install `requirements.txt`, then run:
```bash
python scripts/clinical_statistics_analysis.py --data data/synthetic_clinical_cohort.csv --out reports
```
The script creates cohort summary CSV, OLS summary, JSON results and a figure. It checks identifiers, event coding and time consistency. Results are illustrative and may vary if the dataset or random seed is changed.

## R practical
Open `scripts/clinical_research_workflow.R` and run it from this folder. It uses base R for descriptive analysis and `survival` for Kaplan–Meier/Cox models if the package is installed. The script does not impute missing values or assert causal effects.

## Important
- Use synthetic or approved de-identified data only.
- The generated event indicator is simulated, not a validated clinical endpoint.
- This is an educational example, not a clinical prediction model.
- Review assumptions and clinical context before interpreting any estimate.


## Interpreting the supplied model output
The synthetic event prevalence is low. A default 0.50 classification threshold can produce no positive predictions in the holdout sample even when ROC-AUC is above 0.50. This is intentional teaching material: inspect the confusion matrix, sensitivity, precision-recall curve, calibration and threshold trade-offs. Do not optimise a threshold on the holdout set. The dataset is too small and artificial for clinical deployment.
