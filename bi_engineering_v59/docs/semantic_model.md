# Healthcare BI semantic model

## Model contract
- Fact table: `FactEncounter`; grain is exactly one row per encounter.
- Dimensions: `DimDate` (one row per calendar date), `DimDepartment` (one row per department).
- Relationships: `DimDate[Date]` 1:* `FactEncounter[EncounterDate]`; `DimDepartment[DepartmentKey]` 1:* `FactEncounter[DepartmentKey]`.
- Filter direction: single direction from dimensions to fact by default.
- Keys: integer surrogate keys in dimensions/fact; retain source encounter ID as a degenerate/business identifier.
- Date table: mark as the date table in Power BI; cover the full reporting period and include contiguous dates.

## Metric definitions
| Metric | Definition | Grain / caveat |
|---|---|---|
| Encounter Count | Count fact rows | One row = one encounter |
| Unique Patients | Distinct patient keys | Across selected period; not additive across departments |
| IPD Encounters | Count encounters where type=IPD | Encounter count, not admissions unless source defines it |
| IPD Share | IPD encounters / all encounters | Denominator must follow same filter context |
| Mean IPD LOS | Average LOS among IPD encounters | Validate transfer/readmission rules |
| Total Charges | Sum charge amount | Not revenue, reimbursement or collected cash |

## Security
Use Power BI RLS roles and an identity-to-department mapping table. Test with **View as** for each role and an unprivileged identity. RLS is not a substitute for source-system access controls, workspace permissions or export governance. Avoid dynamic filters based on untrusted free-text inputs.

## Performance checklist
1. Prefer a star schema and integer relationship keys.
2. Remove unused columns and high-cardinality text from fact table.
3. Use explicit measures, not implicit aggregations.
4. Avoid bidirectional relationships unless justified and documented.
5. Inspect Performance Analyzer and model size.
6. Validate filter propagation and totals against SQL.
7. Avoid unnecessary calculated columns; prefer Power Query/source transformations where appropriate.
8. Use incremental refresh only when a reliable date column and policy justify it.

## Import workflow
1. Open Power BI Desktop on Windows.
2. Get Data → Text/CSV → import `data/encounters.csv`.
3. Build or import date and department dimensions; create the relationships above.
4. Rename tables/columns to match `measures.dax` or adapt measure references.
5. Create measures individually from `powerbi/measures.dax`.
6. Mark `DimDate[Date]` as date table.
7. Validate all measures against the SQL view outputs.
8. Save a `.pbix` locally; this package does not include a generated PBIX.
