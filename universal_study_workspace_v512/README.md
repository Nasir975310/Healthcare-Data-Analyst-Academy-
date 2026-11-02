# v5.12.0 — Universal Study Workspace

A disease-agnostic study specification builder for seven common study-design families: observational cohort, case-control, cross-sectional, randomized trial, diagnostic accuracy, case series and registry/longitudinal.

The browser interface captures research question, domain, setting, population, inclusion/exclusion criteria, time definitions and a variable dictionary. It provides design-specific workflow prompts, structural warnings and JSON export.

Run the independent structural validator:
`python scripts/validate_study_spec.py examples/generic_observational_cohort.json`

This is a protocol-planning and learning tool, not a patient-data capture system, ethics approval workflow, sample-size calculator, statistical analysis engine or clinical decision-support product.
