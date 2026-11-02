# Healthcare Data Analyst Academy — v5.17.0

## Healthcare Analytics Research & Publication Workbench

### New capabilities
- Table 1 baseline characteristics generation in CSV and HTML.
- Continuous summaries: mean (SD) or median (IQR); categorical summaries: n (%).
- Optional exploratory Welch/Mann–Whitney and chi-square p-values with limitations documented.
- User-entered CONSORT-style and PRISMA-style SVG participant flow drafts with count consistency validation.
- Concise CONSORT, STROBE cohort and PRISMA 2020 reporting prompts.
- Basic RIS bibliography import to CSV and BibTeX.
- SHA-256 input lineage, publication manifest, and final manuscript quality-control guidance.
- Integrated Academy view with table preview, flow diagrams and interactive checklist selector.

### QA
- v5.17 tests: 5 passed.
- v5.16 regression: 5 passed.
- v5.15 regression: 5 passed.
- v5.14 regression: 4 passed.
- v5.13 regression: 3 passed.
- 95 Python files compiled successfully.
- 228 JSON files parsed successfully.
- New JavaScript passed `node --check`.
- Academy HTML IDs: no duplicates.
- Academy local resource references: no missing paths.
- End-to-end generation completed: Table 1 CSV/HTML, CONSORT SVG, PRISMA SVG, RIS CSV and BibTeX.
- ZIP integrity checked after packaging.

### Scope boundaries
All included data and references are synthetic. The reporting checklists are concise prompts, not full official checklists or compliance certification. Flow diagrams are drafts and require source-record reconciliation and exclusion reasons. RIS import is basic and does not deduplicate or verify references. Statistical choices and manuscript content require protocol, clinical and statistical review.
