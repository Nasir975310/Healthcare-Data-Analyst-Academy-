# Independent portfolio review scorecard

Score each item 0–2: 0 = absent/incorrect, 1 = partial, 2 = complete and evidenced.

| Review item | Score (0–2) | Reviewer evidence / comments |
|---|---:|---|
| Problem statement and decision are explicit | | |
| Population, period, grain and denominator defined | | |
| Data source and provenance documented | | |
| Privacy and permitted-use statement present | | |
| Primary/foreign keys and duplicates checked | | |
| Missingness, ranges and chronology checked | | |
| Join cardinality and fan-out checked | | |
| Orphans retained, quantified and dispositioned | | |
| SQL/Python can be rerun from README | | |
| One headline result independently recomputed | | |
| KPI units, labels and definitions are clear | | |
| Interpretation is proportionate to evidence | | |
| Limitations and unresolved risks are visible | | |
| Executive summary answers the original question | | |
| Handoff states files, version and next action | | |

**Maximum:** 30 points.

- 27–30: strong portfolio candidate, subject to all critical gates.
- 22–26: revise identified weaknesses before public presentation.
- 16–21: substantial revision required.
- 0–15: not yet portfolio-ready.

## Critical gates (must all pass)
- No PHI, confidential data, credentials or personal identifiers exposed.
- No silent deletion of records that materially affect results.
- No unsupported clinical, causal or regulatory claims.
- Reproducibility demonstrated by reviewer or explicitly marked not independently reproduced.
- Any known critical data-quality issue disclosed.

A high numeric score cannot override a failed critical gate. Reviewer identity, date, commit/version and evidence rerun must be recorded.
