# Power BI model implementation specification

## Recommended model
- `FactEncounter`: one row per encounter; grain = encounter_id.
- `DimPatient`: one row per patient_id; keep only approved, necessary attributes.
- `DimDate`: one row per calendar date; mark as date table.
- `DimEncounterType`: one row per normalized encounter type.
- `FactMedicationOrder`: one row per medication order; separate fact, do not join directly to encounters in a way that multiplies encounter counts.
- `DimMedication`: one row per normalized medication/class.

Use one-to-many, single-direction relationships from dimensions to facts. Avoid bidirectional relationships unless a documented requirement proves necessity. Hide technical keys from report consumers. Do not include direct identifiers in published reports.

## Power Query M pattern
Use parameters for file locations; type columns explicitly; trim and normalize categorical strings; preserve source row ID; add `IngestedAt`; route invalid records to a separate query rather than deleting them. Do not use `Table.Distinct` as a silent duplicate fix.

## DAX measures
See `MEASURES.dax`. Measures assume the model names above. Validate each against an independently computed SQL result using identical filters and date boundaries.

## Report pages
1. Executive overview: encounters, unique patients, average encounters per patient, monthly trend.
2. Operations: encounter type and monthly volume.
3. Medication orders: order counts by medication class; clearly label as orders, not dispensing/adherence.
4. Data quality: accepted/rejected counts, exception categories, refresh timestamp.
5. Definitions: KPI descriptions, exclusions, data limitations.

## Performance acceptance
- Use Performance Analyzer for slow visuals.
- Prefer measures over calculated columns where appropriate.
- Avoid high-cardinality text fields in visuals.
- Keep visuals focused; avoid excessive slicers and cross-highlighting.
- Test cold and warm refresh, common filter combinations, and low-memory conditions.
- Record dataset size, refresh duration, visual response time and hardware.
