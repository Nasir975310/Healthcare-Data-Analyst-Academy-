# Portfolio quality gate

A project is portfolio-ready only when every mandatory gate passes.

## 1. Problem definition
- Stakeholder, decision, population, period, grain and denominator are explicit.
- Requirements, assumptions, exclusions and acceptance criteria are recorded.
- KPI definitions are approved or clearly labelled provisional.

## 2. Data governance
- Data source, owner, access basis, refresh date and permitted use are documented.
- No PHI, confidential trial data, secrets, tokens or production identifiers are committed.
- Synthetic data are labelled synthetic; de-identification is not assumed to make data public.

## 3. Technical correctness
- Keys, row counts, joins, missingness, ranges, temporal logic and referential integrity are checked.
- Aggregations respect grain; fan-out and silent row loss are tested.
- SQL and Python can be rerun from documented commands.
- Outputs are reproducible from included inputs or clearly identified source extracts.

## 4. Analytical integrity
- Numerators, denominators, units and time windows are explicit.
- Descriptive association is not presented as causality.
- Uncertainty, missingness, bias and limitations are discussed.
- Clinical measures and operational proxies are not over-interpreted.

## 5. Communication and handoff
- Executive summary answers the original question.
- Charts have titles, units, labels and readable scales.
- Recommendations are proportionate to evidence.
- README explains setup, execution, outputs, QA and limitations.
- A reviewer can reproduce at least one headline result.

## Status labels
- **Draft:** work exists but has not passed all gates.
- **Reviewed:** peer review completed; issues recorded.
- **Reproducible:** another person reran key outputs successfully.
- **Portfolio-ready:** all mandatory gates pass and no sensitive data are exposed.

A self-assigned status is not independent verification. State who reviewed the work and what they reran.
