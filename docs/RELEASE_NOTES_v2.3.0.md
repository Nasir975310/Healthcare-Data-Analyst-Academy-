# Academy v2.3.0 — Power BI and Healthcare Dashboard Laboratory

## Added
- Dedicated Power BI Mastery view with eight progressive applied challenges.
- Seven core model tables plus a separate role-playing order-date dimension (eight CSV model inputs).
- Dimensional model specification and Mermaid diagram.
- DAX measure library for encounter counts, mean LOS, supplied flag proportion, medication order count, quantity, synthetic value and quality exceptions.
- Power Query M import pattern.
- Three-page report blueprint: executive overview, medication utilisation and data quality.
- Importable HDA Clinical Blue Power BI theme.
- Linux Streamlit + Plotly sample dashboard and requirements file.
- Client handoff template and platform guide.
- Local browser progress tracking for Power BI challenges.

## Model controls
- DimEncounter: 80 unique encounter IDs.
- FactEncounterMetrics: 80 rows, one per encounter.
- FactMedicationOrders: 151 rows, one per order source record.
- DimDate and DimOrderDate: 90 rows each; separate role-playing dimensions prevent ambiguous active date paths.
- DimDrug, DimDepartment and DimPayer keys are unique.
- One orphan encounter reference is intentionally retained for data-quality practice.

## Reconciled values
- Mean supplied LOS: 3.875 days.
- Supplied readmission flag: 7/80 = 8.75%; not independently validated.
- Ordered quantity: 3,038.
- Synthetic order value: INR 100,279.75.
- One missing unit cost and one blank therapeutic class.
- Medication orders are not dispensing, administration, adherence or appropriateness evidence.

## Platform limitations
- No PBIX file is generated; Power BI Desktop is required for PBIX authoring and actual DAX/Power Query execution.
- Power BI Desktop is not natively supported on Linux.
- Included Streamlit/Plotly app is a learning alternative, not feature-equivalent to Power BI.
- Streamlit runtime was not installed in the build environment; Python source syntax and model joins were validated, but the interactive app was not launched.
