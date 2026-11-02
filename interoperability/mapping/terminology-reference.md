# Clinical terminology and classification reference

| System | Typical purpose | Common data |
|---|---|---|
| ICD-10 (national modification may vary) | Disease classification, reporting and morbidity coding | Diagnoses and conditions |
| SNOMED CT | Detailed clinical terminology | Clinical findings, disorders, procedures, body structures |
| LOINC | Identifiers for laboratory and clinical observations/documents | Lab tests, measurements, panels |
| RxNorm (US context) | Normalised clinical drug names and relationships | Medication concepts and products |
| ATC | Anatomical Therapeutic Chemical classification | Drug utilisation and therapeutic class analysis |

## Important distinctions
- A code is meaningful only with its code system URI/identifier and relevant release/version.
- Display text is not a reliable unique key.
- Local hospital codes need a governed mapping process.
- LOINC identifies an observation concept; UCUM codes identify units.
- RxNorm is US-oriented; local medication terminology and national regulatory catalogues may be required elsewhere.
- ATC supports drug classification; it is not a complete medication product or prescribing vocabulary.
- SNOMED CT and some terminology distributions have licensing and jurisdictional constraints.

The sample files use familiar example codes for teaching. Verify all terminology mappings against current authoritative releases and local implementation guides before clinical use.
