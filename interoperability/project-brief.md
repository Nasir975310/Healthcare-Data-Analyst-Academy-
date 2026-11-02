# End-to-end hospital interoperability project

## Scenario
A fictional hospital wants an analytics-ready extract combining encounter, medication request and laboratory observation data. Source extracts are synthetic CSVs; FHIR and HL7 fixtures demonstrate message/resource semantics.

## Required deliverables
1. Source inventory and data-flow architecture.
2. FHIR/HL7 field interpretation and reference resolution notes.
3. Terminology crosswalk review with explicit unmapped values.
4. Curated CSV outputs for patient, encounter, medication and laboratory data.
5. Data-quality report with source counts, rejected/quarantined rows and reasons.
6. SQLite warehouse schema and loaded tables.
7. Lineage, data dictionary, governance checklist and client handoff.

## Acceptance
- Source counts reconcile to 80 patients, 120 encounters, 180 medication orders and 220 observations.
- Every foreign reference is valid or appears in a documented quarantine report.
- Duplicate source identifiers are reported.
- Dates and units are preserved and validated.
- Source codes and displays remain traceable after mapping.
- Medication orders are not described as administrations or adherence.
- No real patient information is used.
