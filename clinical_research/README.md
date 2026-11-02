# Clinical Research, Pharmacovigilance and RWE — v2.8.0

## Included training assets
- `data/synthetic_trial_subjects.csv`: 240 synthetic subject-level trial records. One record per subject; this is not a visit-level EDC export.
- `data/synthetic_pv_cases.csv`: 180 synthetic case-level safety records. Event rows are simplified to one coded event per case for teaching; real ICSR systems require richer case/event/product structures and follow-up versioning.
- `scripts/analyse_synthetic_data.py`: reproducible pandas descriptive analysis.
- `challenges.json`: 15 progressive challenges surfaced in the Academy UI.

## Run
From the Academy root, activate your Python environment and run:
```bash
python -m pip install pandas
python clinical_research/scripts/analyse_synthetic_data.py
```
The script prints arm-level descriptive summaries and product/event counts plus basic data-quality checks.

## Important interpretation limits
- The trial dataset is generated for software practice. It is not a clinical trial, not randomisation evidence and not suitable for treatment recommendations.
- The pharmacovigilance data are synthetic. Case counts are not incidence rates because exposure denominators and reporting probabilities are absent.
- Seriousness, severity, expectedness and causality are separate dimensions. Use the applicable reference safety information, regulatory definitions and SOPs in real work.
- MedDRA is proprietary/licensed. No official MedDRA hierarchy or code list is distributed. Generic event labels are placeholders.
- CDISC SDTM/ADaM and ICH E2B(R3) are introduced conceptually only. This pack does not generate compliant datasets/messages or pass official validation.
- ROR/PRR are screening statistics subject to reporting bias, confounding, sparse counts and multiplicity; they do not establish causality.
- PDC/MPR from claims are medication-availability proxies, not proof of ingestion.
- Propensity scores only address measured covariates under assumptions; assess overlap, balance and residual confounding.

## Privacy and professional use
Use synthetic data for portfolio work. Do not place identifiable patient data, confidential trial data, source documents or regulated safety reports in personal repositories or public portfolios. Follow employer procedures, data-use agreements, applicable law, validated-system requirements and current standards versions.
