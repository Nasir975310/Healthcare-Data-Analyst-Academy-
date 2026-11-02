# Healthcare interoperability and warehousing laboratory

This module uses synthetic CSV data and simplified HL7 v2/FHIR fixtures. It is not a FHIR server, interface engine or production clinical integration.

## Run the standardisation pipeline
From this directory:
```bash
python scripts/standardise_clinical_data.py
```
It creates curated CSVs, a reconciliation JSON report, a quality issues CSV and SHA-256 hashes in `reports/`.

## Build a local SQLite warehouse
Create an empty database using DBeaver or Python sqlite3. Execute `sql/warehouse_schema.sql`. Import the curated CSVs using a deliberate key mapping. Patient and department dimensions should be loaded before facts. The schema intentionally does not auto-import files to avoid unsafe implicit type coercion.

## FHIR and HL7 fixtures
- `hl7v2/ADT_A01_synthetic.hl7`
- `fhir/Patient.json`, `Encounter.json`, `MedicationRequest.json`, `Observation.json`, `Bundle-searchset.json`

## Important terminology notes
The sample LOINC and ATC codes are teaching examples and require verification against the appropriate current release and local context. The local-to-SNOMED row is intentionally unmapped. Do not invent mappings.
