# Implementation guide

## Import into Power BI Desktop
1. Extract the Academy ZIP. Open Power BI Desktop and choose **Get data → Text/CSV** for each CSV in `data/`.
2. Alternatively create four blank queries and paste the matching `.pq` file from `power_query/`; change `FolderPath` to the extracted `data` directory.
3. Create `DimDate` and measures from `dax/healthcare_kpi_measures.dax`.
4. Create the relationships exactly as described in `model/semantic_model.md`; set single direction and mark DimDate as date table.
5. Build a report with encounter trend, encounter type, region, drug class and descriptive BP visuals. Add slicers for date, region and encounter type.
6. Validate totals against CSV row counts and test RLS using View As before sharing.

## Recommended pages
- Executive overview: Patients, Encounters, Completed Encounters, Medication Orders; monthly encounter trend.
- Clinical observations: descriptive mean systolic/diastolic values and distribution by encounter type. Display units and denominator.
- Medication utilization: orders by drug class and medication; show counts and share.
- Data quality: unmatched encounter keys, duplicate keys, missingness and refresh timestamp.

## Performance practices
Keep a star schema, use integer surrogate keys for large production models, disable auto date/time, remove unused columns, set correct data types early, prefer measures over calculated columns when aggregation is needed, avoid high-cardinality text in visuals, and inspect Performance Analyzer / DAX Studio query plans. Incremental refresh requires a DateTime RangeStart/RangeEnd parameter and a supported service refresh configuration; it is not activated by these CSV templates.

## RLS and governance
Use least privilege, an explicit user-to-region/facility mapping, and test both positive and negative access. Do not use email strings embedded in DAX as a substitute for a managed security mapping. Never place real patient identifiers in this training project.

## Compatibility
Power BI Desktop is Windows software. On Linux/Ryoku, use Windows in a supported VM or remote Windows environment; Power BI Service authoring capabilities depend on tenant/licensing. The supplied M and DAX are source templates and have not been executed in Power BI Desktop or Service in this environment.
