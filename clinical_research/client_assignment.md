# Portfolio assignment: trial outcomes + safety review + RWE protocol

## Brief
A fictional sponsor asks for a reproducible exploratory review of a synthetic 12-week study and a separate synthetic post-market safety extract. Prepare a concise report for a clinical data and safety review meeting. Do not pool the two datasets or imply that the safety extract provides incidence.

## Required deliverables
1. **Clinical data management:** subject-level data dictionary, grain/key statement, edit-check plan, issue/query log and database-lock readiness checklist.
2. **Trial analysis:** participant flow (where data permit), baseline/endpoint summaries by arm, change-from-baseline analysis with effect estimate and 95% CI, missing-data and attrition discussion, AE descriptive table. State that the synthetic file has one row per subject and no longitudinal visit history.
3. **Pharmacovigilance:** case/event grain design, seriousness vs severity vs expectedness vs causality explanation, duplicate review workflow, product-event count table, ROR/PRR specification with 2x2 cell definitions and sparse-data cautions. Do not call a count a rate or a signal causal.
4. **RWE protocol:** target-trial-style question, new-user active-comparator cohort, eligibility, index date, exposure, follow-up, outcome, censoring, confounder set, propensity-score plan, balance diagnostics and sensitivity analyses.
5. **Quality and handoff:** reproducible scripts/SQL, source-to-output lineage, validation log, limitations, executive summary and next-step recommendation.

## Scoring rubric (100 points)
| Domain | Points |
|---|---:|
| Data model, grain, data dictionary and provenance | 10 |
| Trial cleaning, missingness and query controls | 15 |
| Trial analysis, uncertainty and interpretation | 15 |
| ICSR workflow and safety concept accuracy | 15 |
| Signal-screening methods and limitations | 10 |
| RWE cohort design, time zero and bias control | 20 |
| Reproducibility, QA and professional handoff | 15 |
| **Total** | **100** |

## Critical errors (require revision regardless of score)
- Treating seriousness and severity as synonyms.
- Reporting spontaneous-report case counts as incidence.
- Describing disproportionality as proof of causality.
- Claiming PDC/MPR proves ingestion.
- Ignoring immortal-time bias or defining time zero inconsistently.
- Claiming CDISC, MedDRA or E2B(R3) conformance without validated evidence and appropriate licensed/versioned resources.
- Using real patient or confidential trial data in a public portfolio.
