# Power BI semantic model

## Grain and relationships
- DimPatient: one row per PatientID; 1:* to FactEncounter.
- DimDate: one row per date; 1:* to FactEncounter on EncounterDate (active).
- FactEncounter: one row per EncounterID; 1:* to FactObservation and FactMedication on EncounterID.
- FactObservation: one row per ObservationID.
- FactMedication: one row per MedicationID. Add PatientID to FactMedication by merging with FactEncounter in Power Query only if required for analysis.

Use single-direction dimension-to-fact relationships. Do not directly join the two child fact tables; that creates row multiplication (fanout). Use explicit measures, not implicit sums. Mark DimDate as the date table.

## RLS
Create roles using a controlled security mapping table (UserPrincipalName to Region or FacilityID), filter the dimension, and test allowed/denied users with View As. Hidden pages/columns are not security. Do not publish patient-level data in public portfolios.

## Clinical interpretation
BP summaries are descriptive synthetic readings. A threshold flag is not a diagnosis, BP-control rate, guideline target, or treatment recommendation.
