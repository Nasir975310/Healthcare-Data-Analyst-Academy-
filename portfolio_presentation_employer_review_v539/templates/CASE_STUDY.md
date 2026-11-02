# Case study: Synthetic outpatient operations analytics

> Replace every instruction below with evidence from your own latest run. Do not invent results.

## Executive summary
- **Question:** What operational patterns can be summarized from the synthetic encounter data?
- **Audience:** [e.g. outpatient operations manager]
- **Dataset:** [synthetic source, row count, date range if present]
- **Result:** [one verified finding with exact output reference]

## Problem and scope
[Describe the decision question and what is explicitly out of scope.]

## Data model and preparation
[State row grain, primary key, fields, transformations, duplicate policy, missingness and exception handling.]

## Methods and metric contract
| Metric | Definition | Numerator / population | Denominator / valid n | Exclusions |
|---|---|---|---|---|
| Mean wait time | Arithmetic mean of valid wait minutes | Sum of valid wait minutes | Count of valid wait values | Missing/negative values |

## Results
[Insert verified tables or charts. Link each value to a generated artifact.]

## Quality assurance
[Report test command and result, row reconciliation, database integrity and output manifest.]

## Limitations
- Synthetic data; not representative of a real hospital.
- Small demonstration dataset; no population inference.
- Operational summaries do not establish causality or clinical outcomes.
- [Add project-specific limitations.]

## Reproducibility
[Exact environment, commands, commit/archive identifier and outcome.]

## What I would do next
[Stakeholder validation, larger authorized dataset, privacy review, workflow integration and monitoring.]

## Evidence index
| Claim | Artifact | Verification |
|---|---|---|
| [claim] | [relative path] | [test, command or manual check] |
