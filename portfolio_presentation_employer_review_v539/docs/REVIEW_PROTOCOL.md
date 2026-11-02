# Employer-style review protocol

## Review question
Could a junior healthcare data analyst explain, reproduce and defend this work with a reviewer watching?

## Review sequence
1. **Inspect the repository**: file structure, README, dependencies, license, data provenance, privacy and secret hygiene.
2. **Trace one metric** from raw row to validation rule, curated dataset, SQL/Python aggregation, output and narrative.
3. **Challenge the grain**: identify what one row represents in each table and whether joins can multiply records.
4. **Challenge the denominator**: confirm inclusion/exclusion criteria, missingness and valid observation counts.
5. **Reproduce**: run the documented commands from a fresh directory; compare key outputs and hashes where deterministic.
6. **Review communication**: compare every case-study number with generated outputs; inspect caveats and avoid causal/clinical claims.
7. **Interview**: ask the author to explain one defect, one design decision and one limitation.

## Evidence hierarchy
- Strong: command output, test output, generated report, reproducible hash, screenshot with context.
- Moderate: source code and a documented manual check.
- Weak: an unchecked checklist, unsupported prose, a badge, or a claim without a linked artifact.

## Scoring rubric (100 points)
| Domain | Points | What earns full credit |
|---|---:|---|
| Data integrity and privacy | 20 | Synthetic/licensed provenance, documented grain, constraints, exceptions, no secrets or PHI |
| Method and metric validity | 20 | Explicit numerator/denominator, exclusions, missingness, correct aggregation |
| Technical quality | 20 | Readable code, meaningful tests, reproducible environment, traceable outputs |
| Communication | 15 | Concise case study, accurate visuals/tables, limitations, stakeholder relevance |
| Reproducibility and evidence | 15 | Clean-clone run, command log, test results, output hashes |
| Interview defensibility | 10 | Clear explanation of trade-offs and ability to debug |

### Interpretation
- 85–100: strong portfolio candidate, subject to human review.
- 70–84: presentable with targeted corrections.
- 50–69: substantial gaps; revise before promoting.
- Below 50: not ready for public portfolio use.

**Hard gates:** any real patient-identifiable information, exposed credentials, fabricated results, or knowingly misleading clinical claims means **do not publish**, regardless of score. A numerical score is a structured review aid, not a hiring prediction.

## Reviewer notes
Record the exact commit/archive reviewed, environment, commands, date, reviewer identity (if appropriate), findings and unresolved limitations. Never describe a self-review as an independent employer review.
