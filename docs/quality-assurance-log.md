# Quality assurance log — Release 1.1.0

## Scope
Completes Volume 3 Chapters 11–14: R data analysis/visualization, reproducible reporting, automation/reusable code and the integrated Python/R/SQL portfolio. Adds R scripts, Quarto source, a Python CLI pipeline, automated tests, SQL reference, report and handoff materials.

## Checks performed
- Curriculum, lessons and glossary JSON parsed successfully.
- Authored lesson count: 42/111 (Volume 1 14/14; Volume 2 14/14; Volume 3 14/14).
- All 42 authored lessons contain learning outcomes, at least five structured sections and at least three exercises with worked answers.
- All 42 assessment files parsed; answer indexes and explanations checked.
- Python CLI pipeline executed successfully against the synthetic dataset.
- Pipeline control totals: 104 encounters; 60 distinct patients; 96 nonmissing SBP; 8 missing SBP; zero unmatched departments; department total 104.
- Seven Python unit tests passed, covering unique keys, duplicate rejection, date boundaries, invalid date range, missingness preservation, department reconciliation and duplicate lookup rejection.
- Static Markdown report generated from pipeline outputs.
- Python source syntax compilation and JavaScript syntax check performed.
- ZIP archive integrity and required file presence checked.

## Methodology and safety controls
- The main analysis grain is one row per encounter.
- Reporting interval is 2026-01-01 inclusive to 2026-04-01 exclusive.
- Missing SBP values remain missing and are excluded only from SBP-specific calculations.
- Department lookup is validated as many-to-one and row count is reconciled.
- Cross-tool comparisons require identical cohort dates and metric denominators.
- The report states synthetic-data and non-causal interpretation limits.
- No real patient identifiers or credentials are included.

## Limitations not to conceal
- Rscript was unavailable in the release-generation environment. R scripts were authored but not executed.
- Quarto CLI rendering was not performed; the `.qmd` source is included with run instructions.
- The Python Quarto document and R package requirements may need adjustment to the user's local versions.
- Browser automation and exhaustive manual cross-device QA have not been performed.
- No accredited credential or job placement is provided; assessments are formative.
- Synthetic data are not suitable for clinical inference, patient care, benchmarking or model training.

## Release v1.2.0 — Volume 4 milestone

- Authored all 13 mapped Volume 4 chapters: research questions, study designs, sampling/power, comparative methods, regression, survival analysis, diagnostic accuracy, missing data, bias/confounding, systematic reviews/meta-analysis, trial data workflows, evidence interpretation and reproducible research.
- Added 52 worked exercises and 78 formative assessment items.
- Expanded glossary to 163 terms.
- Added a 240-record synthetic cohort capstone, data dictionary, project brief, reproducible pandas analysis script and generated summary/missingness/validation outputs.
- QA passed: lesson and assessment JSON parsing; chapter structure; answer-key index checks; Python capstone pipeline execution; 240-row summary reconciliation.
- Limitations: R and Quarto execution are not claimed for this milestone; browser/device QA remains outstanding. Synthetic cohort is educational only and must not be used for clinical decisions or publication.

## Release v1.3.0 — Volume 5 milestone

- Authored all 15 Volume 5 chapters: EHR architecture, clinical terminology, laboratory data, medication data, drug utilisation, pharmacovigilance, quality outcomes, hospital operations, population health, RWD/RWE, HL7/FHIR, OMOP CDM, clinical decision support, Indian digital-health context and integrated capstone.
- Added 60 worked exercises and 90 formative assessment questions.
- Expanded glossary to 179 terms.
- Added an integrated synthetic capstone with 180 patients, 300 encounters, 500 medication order lines and 420 laboratory result rows.
- Executed pandas pipeline successfully. Primary keys were unique; foreign keys reconciled; discharge dates were valid; departmental, medication and laboratory summaries were generated.
- Limitations: synthetic data only; no real clinical inference. No official ABDM implementation or live FHIR integration is included. R/Quarto execution and browser/device QA remain outstanding.

## Release v1.4.0 — Volume 6 milestone

- Authored all 14 Volume 6 chapters: BI requirements and KPI contracts; Power BI; star schemas and DAX; dashboard governance; Tableau and Linux-compatible alternatives; ETL/ELT; warehouses/lakes/lakehouses; Git collaboration; Linux workflows; REST APIs; Docker; cloud/IAM; data governance/observability; production handoff.
- Added 56 worked exercises and 84 formative assessment questions.
- Expanded glossary with 30 BI/data-engineering terms.
- Added Linux-first BI/data engineering capstone with 150 synthetic patients, 500 encounters and 900 medication order lines.
- Executed pandas pipeline successfully: primary keys unique, foreign keys reconciled, encounter totals reconcile to 500 and medication totals reconcile to 900.
- Power BI Desktop is explicitly documented as Windows-only/not natively supported on Linux; local Linux alternatives and Windows/managed environment options are described.
- Limitations: no Power BI PBIX file generated; no live cloud/API integration; Dockerfile authored but image build not executed in this QA; R/Quarto and browser/device QA remain outstanding.


## Cross-platform curriculum requirement
- Added `docs/cross-platform-learning-standard.md` as the mandatory Linux + Windows teaching specification.
- Added a prominent pointer in the Academy README.
- Applies to all existing and future volumes: relevant chapters must provide separate setup, commands, execution, expected output, troubleshooting, and verification for both operating systems.
- This is a curriculum standard, not a claim that every chapter has already been retrofitted or manually tested on both operating systems. Existing chapters will be brought into compliance as they are revised; future chapters must meet the acceptance criteria before being marked complete.


## Release 1.5.0 — Volume 7 and Linux/Windows retrofit
- Authored V07 Chapters 01–13 with structured learning outcomes, topic sections, exercises, cross-platform practicals, troubleshooting, handoff guidance and clinical-safety callouts.
- Added 13 six-question formative quizzes.
- Added cross-platform execution sections to all 84 previously authored V01–V06 lessons (plus all 13 V07 lessons).
- Added `projects/v07_predictive_analytics_capstone/` with synthetic data generation, validation checks, scikit-learn pipelines, metrics, run metadata and separate Bash/Fish/PowerShell setup instructions.
- Executed `run_capstone.py` successfully in the artifact environment: 2,400 synthetic patients; 1,800 training and 600 test records; unique IDs and binary outcome checks passed; metrics and validation files generated.
- Runtime test environment: Python and scikit-learn available. This does not constitute a Windows execution test. Windows instructions are authored but require user-side validation on a Windows machine.
- Limitations: capstone is a synthetic educational prototype; one row per synthetic patient; no external validation, prospective evaluation, clinical utility analysis, fairness certification or deployment. The 0.5 threshold is illustrative only.
- No claim of full browser/device QA or manual dual-OS testing. Existing chapter command blocks and new instructions require validation against the learner's actual OS versions and tool installations.


## Release 1.6.0 — Volume 8 and curriculum completion
- Authored V08 Chapters 01–14 with learning outcomes, detailed topic sections, exercises, cross-platform execution, troubleshooting and professional evidence guidance.
- Added 14 six-question formative assessments (84 questions).
- Added career-launch toolkit: job application tracker, skills evidence matrix, 90-day plan, portfolio checklist, proposal template, mock interview bank and final readiness scorecard.
- Updated all 111 curriculum coverage rows to authored.
- Dual-OS instructions are authored across all 111 chapters. They have not been manually executed on every supported Linux distribution and Windows release; Windows execution remains unverified in this generation environment.
- No live job vacancies, salary claims or credential prices are embedded. Learners must verify current role eligibility, exam costs, terms and regulatory requirements using official sources.
- Career readiness scorecard is educational self-assessment only; no accreditation, certification or job guarantee is claimed.


## v1.8.0 — Volume 7 and 8 worked-solution retrofit
- Scope: 27 chapters, 108 exercise answers.
- Replaced generic guidance with specific model answers, formulas, worked calculations, code/pipeline patterns, evaluation logic and professional safeguards.
- Automated content check: all 108 answers present; no generic template phrases detected; minimum answer length 387 characters.
- Limitation: authored content has not undergone independent clinical/statistical peer review. Verify local policies, package versions, regulatory requirements and current job-market information before operational use.


## Release 1.9.0 — practical laboratory retrofit
- Added 8 structured practical labs with objective, deliverable, prerequisites, Linux/Fish and Windows/PowerShell commands, ordered steps, acceptance criteria, troubleshooting, precautions and portfolio evidence.
- Added searchable Practical Labs navigation and expandable lab details to the offline HTML app.
- Reused existing synthetic project assets; no real patient data added.
- Cross-platform commands are authored, not represented as executed on Windows.
- Browser runtime interaction and cross-device sync are not claimed as tested.


## Release 2.0.0 — job simulations
- Added 3 structured employment simulations covering Excel reporting, SQL analytics and an end-to-end remote client request.
- Added 80 synthetic encounter rows and 150 synthetic medication-order rows, an Excel workbook, SQL starter/solution and client handoff templates.
- Added searchable Job Simulations UI with scenario, requirements, OS-specific launch commands, deliverables, 100-point rubric, acceptance criteria and pitfalls.
- Data grain and interpretation cautions are explicit: encounter vs order; orders are not administrations; synthetic readmission flag is not validated.
- Cross-platform instructions are authored; Windows execution is not independently claimed.

- Data validation: 80/80 encounter IDs unique; 150/150 order IDs unique.
- SIM-02 worked SQL executed against the supplied CSV data loaded into SQLite; all four solution queries returned successfully.
- SIM-01 reference metrics independently calculated: 7/80 supplied readmission flags (8.75%); mean LOS 3.875 days.
- Excel workbook opened and inspected programmatically; expected sheets and row counts confirmed.


## Release 2.1.0 — Healthcare SQL Mastery
- Added 11 progressive SQL challenges with starter query, hint, worked solution, expected output and validation explanation.
- Added searchable SQL Mastery interface, reveal-on-demand hints/solutions and browser-local completion tracking.
- Created ready-to-query SQLite database with 80 synthetic encounters and 150 synthetic medication orders; key constraints and indexes included.
- Executed challenge reference queries against the packaged SQLite database. Verified outputs: 80 encounters, 150 orders, 70 encounters with orders, 10 without, supplied readmission flag 7/80 (8.75%), zero duplicate keys, zero invalid chronology and zero orphan orders.
- SQL query plan inspected; composite class/status index was used by SQLite on this dataset.
- SQL execution occurs in DBeaver/SQLite; browser app does not execute SQL.

- Final SQL Mastery QA: all 11 reference solutions executed successfully against the packaged database; SQL-11 query plan uses the composite class/status index. Challenge UI JSON schema and app JavaScript syntax checks passed.
\n\n## v2.5.0 — Advanced SQL and Database Engineering\n\n- Added PostgreSQL setup, schema, synthetic seed, 10 challenge records, advanced SQL, performance, objects/transactions, security/backup, Python connector demo and client rubric.\n- Reconciled seed source: 80 encounters, 150 orders, 5 departments, 28 distinct drug/route/class tuples.\n- PostgreSQL binaries unavailable; no live PostgreSQL execution claimed. Docker unavailable; compose not launched.\n- Static checks: JavaScript syntax, HTML parser, JSON, Python AST, file references and ZIP integrity. Windows and browser interaction not tested.\n\n\n## v2.6.0 — Statistics, Epidemiology and Clinical Research\n\n- Added 12 challenge records, 400-row synthetic cohort, Python and R workflows, study-design reference, reporting checklist, client brief and scoring rubric.\n- Python analysis executed successfully in build environment; outputs generated.\n- JavaScript syntax, JSON, Python AST and HTML static checks performed. R, Windows and browser automation not executed.\n- Synthetic event prevalence is low; default 0.50 logistic threshold may predict no positive cases. The release documents this as a model-evaluation teaching point, not a successful clinical classifier.\n\n\n## v2.7.0 — Healthcare Data Warehousing and Interoperability\n\n- Added 12 challenge records, synthetic source extracts (80 patients, 120 encounters, 180 orders, 220 observations), HL7 v2 and FHIR fixtures, terminology crosswalk materials, warehouse design and Python standardisation pipeline.\n- Pipeline executed; source and curated counts reconciled; zero orphan references in the clean fixture set.\n- Python AST, JavaScript syntax, JSON and HTML static checks performed. No official FHIR/HL7 validator, live terminology service, browser automation or Windows test was available.\n- Terminology codes are examples and not certified mappings; no production interoperability claim.\n