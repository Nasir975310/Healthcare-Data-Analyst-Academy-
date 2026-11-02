# Quality assurance log — v2.3.0

## Executed checks
- [x] Eight challenge definitions parse and have unique IDs.
- [x] Seven model source tables plus role-playing order-date table generated.
- [x] DimEncounter encounter_id unique (80 rows).
- [x] FactEncounterMetrics encounter_id unique (80 rows).
- [x] FactMedicationOrders order_id unique (151 rows).
- [x] DimDrug, DimDepartment, DimPayer and both date dimension keys are unique.
- [x] One orphan order encounter key retained and counted.
- [x] Mean LOS, supplied flag count/rate, ordered quantity and synthetic order value independently reconciled.
- [x] New Power BI JavaScript passed `node --check`.
- [x] Power BI challenge JSON parsed.
- [x] Academy HTML parsed with Python HTMLParser.
- [x] Streamlit dashboard Python source passed Python AST syntax parsing.

## Not tested / limitations
- Power BI Desktop was not available: PBIX authoring, DAX execution, Power Query M execution, report interactions and PDF export were not tested.
- Streamlit was not installed in the build environment: the local dashboard was not launched or browser-tested. Plotly was available; the Streamlit dependencies are listed in `requirements-powerbi-linux.txt`.
- No Windows execution or cross-device browser automation was performed.
- The model relationship file is a specification; implement and verify relationships in Power BI Desktop.
- No clinical validation or independent peer review of synthetic data assumptions was performed.

## Data interpretation safeguards
- Data is synthetic.
- The readmission flag is supplied and not independently validated.
- Medication orders do not prove dispensing, administration, adherence or appropriateness.
- Unit costs are synthetic.
- The orphan encounter key is intentionally retained for QA training.
