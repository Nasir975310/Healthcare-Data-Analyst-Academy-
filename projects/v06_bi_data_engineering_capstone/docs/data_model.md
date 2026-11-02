# V06 model grain and relationships

```text
DimPatient (1) ---- (*) FactEncounter (1) ---- (*) FactMedicationOrder
                         |
                         +---- DimDepartment
                         +---- DimSite
                         +---- DimDate
```

- `patients.csv`: one row per patient (`patient_id` primary key).
- `encounters.csv`: one row per encounter (`encounter_id` primary key; `patient_id` foreign key).
- `medication_orders.csv`: one row per medication order (`order_id` primary key; `encounter_id` foreign key).

Do not join all raw rows and then count encounters: each encounter can have multiple medication orders. Use separate fact tables or aggregate orders to encounter grain before joining.
