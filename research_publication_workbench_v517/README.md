# v5.17.0 — Healthcare Analytics Research & Publication Workbench

## Quick start
```bash
python -m pip install -r requirements.txt
python scripts/publication_workbench.py \
  --input data/synthetic_publication_dataset.csv \
  --outdir outputs \
  --group arm
```
Optional flow diagrams and RIS import:
```bash
python scripts/publication_workbench.py \
  --input data/synthetic_publication_dataset.csv \
  --outdir outputs \
  --consort-counts 80 40 40 38 39 35 36 36 37 \
  --prisma-counts 500 80 420 350 70 25 45 \
  --ris data/sample_references.ris
```
The script creates Table 1 CSV/HTML, publication manifest JSON, optional CONSORT/PRISMA SVG diagrams and optional RIS-derived CSV/BibTeX files.

## Included
- Baseline characteristics table with continuous and categorical summaries.
- Optional Welch or Mann–Whitney for continuous variables; exploratory chi-square for categorical variables.
- User-entered CONSORT-style and PRISMA-style flow diagram counts with logical validation.
- Concise CONSORT, STROBE and PRISMA 2020 planning checklists.
- Basic RIS import to CSV and BibTeX.
- Publication workflow and QA guide.
- Browser-based reporting checklist and table preview.

## Limitations
All example data are synthetic. This is not a complete manuscript authoring or submission system. Flow diagrams are drafts and omit detailed reasons for exclusion/loss. Checklists are abbreviated planning prompts, not official full checklists or compliance certification. RIS parsing is basic and does not deduplicate or verify references. P-values are exploratory unless prespecified; sparse categorical data require appropriate methods. Review all output against the protocol, source records and journal requirements.
