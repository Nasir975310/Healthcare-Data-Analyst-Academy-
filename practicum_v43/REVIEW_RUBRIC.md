# Reviewer scoring rubric — 100 points

| Dimension | Points | Strong performance |
|---|---:|---|
| Scope and metric definitions | 10 | Decision, population, grain, period, numerator/denominator and exclusions are explicit |
| Data quality and governance | 15 | Keys, missingness, duplicates, chronology, plausibility and privacy are handled transparently |
| Technical correctness | 20 | SQL/Python/Excel/BI logic matches the stated grain; joins and calculations are validated |
| Statistical/clinical interpretation | 15 | Methods fit the question; uncertainty and confounding are considered; no unsupported causal claims |
| Communication and visuals | 15 | Audience-appropriate, readable, decision-focused and denominator-aware |
| Reproducibility | 15 | Raw inputs preserved, code/queries run, dependencies and steps documented, outputs reconciled |
| Handoff and professionalism | 10 | Clear version, limitations, outstanding risks, acceptance request and next steps |

## Decision bands
- **90–100: Reviewer-ready** — no critical blocker; independently reproduce before publication.
- **80–89: Strong draft** — minor repairs; document reviewer comments and resolve.
- **70–79: Conditional** — substantive gaps; revise and resubmit.
- **Below 70: Not accepted** — rebuild core analysis and evidence.
- **Automatic hold regardless of score:** PHI exposure, fabricated results, broken denominator/grain, untraceable transformations, unsupported clinical or causal claims, or inability to reproduce a key result.

## Evidence rules
A self-rating is not reviewer verification. A task is evidence-backed only when a reviewer can inspect the actual file/output and rerun or trace the result. Record exact filenames, commit/hash, run command, software version and reviewer/date. Never upload patient-identifiable material to a public portfolio.
