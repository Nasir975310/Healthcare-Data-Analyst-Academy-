# Power BI semantic model — relationship specification

Use **Model view** and create these relationships. Set cross-filter direction to **Single** unless a specific lab explicitly justifies another direction.

| One side | Many side | Cardinality | Active | Purpose |
|---|---|---|---|---|
| DimDepartment[department_key] | DimEncounter[department_key] | 1:* | Yes | Department attributes filter encounters and their orders |
| DimPayer[payer_key] | DimEncounter[payer_key] | 1:* | Yes | Payer attributes filter encounters and their orders |
| DimEncounter[encounter_id] | FactEncounterMetrics[encounter_id] | 1:1 | Yes | Encounter-level LOS and supplied flag metrics |
| DimEncounter[encounter_id] | FactMedicationOrders[encounter_key] | 1:* | Yes | Encounter-level drill/filter to order rows |
| DimDrug[drug_key] | FactMedicationOrders[drug_key] | 1:* | Yes | Drug and therapeutic-class analysis |
| DimDate[date] | DimEncounter[admission_date] | 1:* | Yes | Admission-date analysis |
| DimOrderDate[date] | FactMedicationOrders[order_date] | 1:* | Yes | Order-date analysis |

## Model design notes
- `DimEncounter` is a conformed encounter dimension with exactly one row per encounter. It carries patient, department, payer, age and admission date attributes.
- `FactEncounterMetrics` has one row per encounter and stores length of stay and the supplied readmission flag.
- `FactMedicationOrders` has one row per medication-order source record. It contains 151 rows and retains the deliberately orphaned encounter key for data-quality analysis.
- `DimDate` and `DimOrderDate` are role-playing date dimensions with the same calendar rows. This avoids two active paths from date to medication orders (directly and through DimEncounter). Use `DimDate` for admission-date analysis and `DimOrderDate` for order-date analysis.
- `DimDrug` is a cleaned training lookup. Blank therapeutic class is retained as a blank/unknown mapping for quality review.
- Do not join the two fact tables directly. Filter them through `DimEncounter`.
- The 1:1 relationship may be represented as 1:* by Power BI depending on model settings; uniqueness of both keys must be checked before creating it.
- The `DimDate` to `DimEncounter` and `DimDate` to `FactMedicationOrders` paths both exist. Avoid ambiguous alternate paths; keep the model single-direction and test each date slicer.
