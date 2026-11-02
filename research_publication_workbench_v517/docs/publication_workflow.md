# Research publication workflow

## 1. Lock the analysis inputs
- Use a final, validated analysis dataset and retain its data dictionary.
- Confirm participant flow, study groups, outcome definitions, missingness and exclusions against source records.
- Record the input SHA-256 and software/package versions.
- Keep synthetic training datasets separate from real clinical data.

## 2. Table 1
- Choose continuous summaries based on distribution and protocol: mean (SD) or median (IQR).
- Report categorical values as n (%), with denominators made clear.
- Display missing values explicitly or report missingness in a separate column.
- Baseline p-values are not universally recommended. Many randomized-trial reporting standards emphasize descriptive baseline differences rather than significance tests. If included, prespecify and explain them.
- For sparse categorical cells, do not rely automatically on Pearson chi-square; select a suitable exact method with statistical review.
- The included generator is a draft formatter. It does not decide the scientifically correct summary or test for every variable.

## 3. Participant flow
- CONSORT-style counts are entered by the analyst and must reconcile with the approved protocol and participant disposition records.
- Include reasons for exclusion, losses to follow-up, withdrawals and analysis exclusions in the final diagram; this draft generator leaves those details for completion.
- PRISMA flow counts must distinguish records, reports and studies. Avoid treating these units as interchangeable.

## 4. Reporting checklists
- CONSORT applies to randomized trials; STROBE applies to observational cohort, case-control and cross-sectional studies; PRISMA 2020 applies to systematic reviews.
- The bundled lists are concise planning prompts, not the full official checklists. Obtain the current official checklist and complete every item against the manuscript.
- A checked item means reviewed by the author; it is not an automated compliance verdict.

## 5. References
- Import RIS and inspect the exported CSV/BibTeX.
- Verify bibliographic metadata, DOI resolution, author order, journal title, year, volume, issue, pages and citation style against authoritative source records.
- Do not fabricate missing metadata. This basic importer does not deduplicate or resolve references online.

## 6. Final quality control
- Reconcile every number across abstract, text, tables, figures and supplements.
- Confirm denominators, units, confidence intervals, decimal places and effect directions.
- Check that methods match results and that all outcomes/analyses are reported.
- Review ethics, consent, trial registration, protocol availability, funding and conflicts of interest.
- Obtain appropriate clinical, statistical and journal/editorial review before submission.
