# Client brief — fictional regional teaching hospital

**Client:** Meridian Teaching Hospital (fictional)  
**Project:** Monthly operations and medication-utilization reporting  
**Audience:** Operations lead, pharmacy lead and data-quality coordinator  
**Data period:** 1 January–30 April 2026  
**Purpose:** Build a reproducible training report from four synthetic CSV extracts.

## Business questions
1. How many patients and encounters are represented?
2. How does encounter volume and status vary by month?
3. Which encounter types account for the greatest activity?
4. What is the medication-order mix by drug class?
5. What do the available BP observations show descriptively?
6. Which source-data issues must be resolved before operational reporting?

## Scope
- Profile source files and document grain, types, keys, missingness and referential integrity.
- Preserve source files and generate a SHA-256 manifest.
- Load staging and curated SQLite tables.
- Exclude invalid/orphan records from curated facts while preserving exception evidence.
- Produce KPI extracts, a data-quality report, SQL and a client-ready narrative.
- Specify a Power BI dashboard and acceptance tests.

## Out of scope
Clinical decision support, hypertension diagnosis, treatment evaluation, medication adherence, dispensing confirmation, patient-level recommendations, production EHR integration, validated regulatory reporting and live patient data.

## Acceptance criteria
- Every source file has row counts and SHA-256.
- Primary keys are unique or exceptions are reported.
- Orphan patient/encounter references are identified and not silently dropped.
- Curated warehouse passes SQLite integrity and FK checks.
- KPI denominators and grains are documented.
- Observation and medication facts are not joined directly in a way that causes fanout.
- Dashboard totals reconcile to curated SQL outputs.
- Report identifies synthetic data, limitations and outstanding data requests.
