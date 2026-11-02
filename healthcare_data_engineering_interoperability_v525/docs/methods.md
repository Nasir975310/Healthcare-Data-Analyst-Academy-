# Methods and limitations

The pipeline ingests a synthetic FHIR R4 Bundle subset (Patient, Encounter, Observation, MedicationRequest), performs local structural checks, flattens resources into separate tables, applies explicitly illustrative local terminology mappings, runs reconciliation checks, builds one row per patient-encounter, constructs a configured encounter-status cohort, and exports CSV, SQLite, JSON reports and SHA-256 hashes.

## Interoperability boundaries
This is not full FHIR R4 validation. It does not load official StructureDefinitions or profiles and does not validate every cardinality, invariant, extension, datatype, transaction, contained resource or canonical reference. ICD-10, SNOMED CT and LOINC are discussed as terminology systems; no authoritative crosswalks are bundled. Example LOINC-to-local labels are educational only. Real deployments require maintained terminology releases, provenance, mapping relationships, licensed content where applicable, terminology services and clinical governance.

## Analytical boundaries
The longitudinal table grain is one row per patient-encounter. Child resources are aggregated to avoid Cartesian multiplication. The numeric observation mean is a convenience field and must not be analysed across mixed analytes or units. Use the Observation fact table with explicit analyte, unit and time-window selection. The cohort uses encounter status and encounter start; it is not a causal treatment cohort.

All data are synthetic. This teaching tool is not clinical decision support and is not approved for identifiable patient data. Production needs security, access controls, encryption, audit, retention, approvals, source reconciliation and validated terminology services.
