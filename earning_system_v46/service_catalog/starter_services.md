# Entry-level healthcare analytics services — safe scope boundaries

These are service concepts to validate with actual buyers. Do not represent yourself as an experienced consultant before you have evidence and supervision appropriate to the work.

## 1. Spreadsheet and CSV quality audit
**Possible deliverable:** column profile, missingness/duplicate report, key/chronology checks, exception file, short QA memo.  
**Tools:** Python/pandas or spreadsheet software.  
**Boundary:** do not change clinical records; do not decide clinical validity.

## 2. SQL reporting and reconciliation
**Possible deliverable:** documented query, grouped summary, reconciliation checks, query README.  
**Tools:** SQLite/PostgreSQL.  
**Boundary:** require authorised access and approved environment; no PHI in public portfolio.

## 3. Dashboard KPI definition and QA
**Possible deliverable:** metric contract, denominator review, filter/total test checklist, dashboard critique.  
**Tools:** Excel/Power BI or local alternatives.  
**Boundary:** do not claim validated clinical outcome metrics without approved definitions and validation.

## 4. Synthetic-data portfolio case study
**Possible deliverable:** reproducible analysis, dashboard, data dictionary, README, limitations.  
**Tools:** SQL, Python, Excel, BI.  
**Boundary:** synthetic data only; do not imply a fictional client or production deployment.

## 5. Research and clinical data cleaning support
**Possible deliverable:** data dictionary, query log, cleaning script, missingness report.  
**Boundary:** protocol, ethics, consent, access, validation and sponsor requirements govern the work. No independent clinical decisions or unauthorized re-identification.

## Avoid initially
- Independent diagnosis, treatment or medication recommendations.
- Safety signal conclusions or regulatory submissions without qualified oversight.
- Clinical efficacy claims from uncontrolled observational data.
- Production EHR/claims integration without formal authorization and security review.
- Promising savings, revenue lift, regulatory compliance or patient outcome improvement without verified evidence.
