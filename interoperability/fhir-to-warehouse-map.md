# FHIR-to-warehouse mapping design

| FHIR resource | Suggested staging grain | Analytics target | Key considerations |
|---|---|---|---|
| Patient | One resource version per Patient id | DimPatient | Business identifiers, active status, version history, identity governance |
| Encounter | One Encounter resource/version | FactEncounter | Status lifecycle, class, period, subject reference, encounter type |
| MedicationRequest | One MedicationRequest resource/version | FactMedicationRequest | Request != administration; dosage, status, medication coding |
| Observation | One Observation resource/version | FactObservation | Code, value, unit, effective time, status, interpretation |

## Mapping controls
- Preserve FHIR logical id and source server/base URL.
- Preserve `meta.versionId` and `meta.lastUpdated` where available.
- Resolve references using server identity plus resource type/id; never assume local IDs are globally unique.
- Distinguish `CodeableConcept.text` from codings.
- Preserve all relevant codings and their systems; do not collapse multiple codings into one text label.
- Normalise Quantity with original value, unit, UCUM code and conversion metadata if converted.
- Handle resource status and deletion/tombstone events.
- Decide whether analytics requires current-state or historical/as-of records.
