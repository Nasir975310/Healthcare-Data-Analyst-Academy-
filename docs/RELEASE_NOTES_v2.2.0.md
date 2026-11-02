# Academy v2.2.0 — Advanced Excel and Power Query Laboratory

## Added
- Dedicated searchable Excel Mastery view with eight progressive challenges.
- Worked formulas and patterns for IF, COUNTIF/COUNTIFS, SUMIFS, AVERAGEIFS, IFERROR, XLOOKUP and INDEX/MATCH.
- PivotTable/PivotChart workflow, data validation, conditional formatting and dashboard exercises.
- Power Query cleaning challenge with a supplied M reference script and explicit warning that the M script was not executed in Power Query Desktop.
- Linux alternative using LibreOffice Calc plus a runnable Python/pandas cleaning script.
- Synthetic Excel workbook with eight worksheets: START_HERE, Raw_Encounters, Raw_Orders, Formulary, Tasks, Formula_Practice, Data_Dictionary and Reference_Checks.
- Three CSV inputs, data dictionary, duplicate-candidate review output, and a 45-minute client simulation with a 100-point rubric.
- Browser-local challenge completion and a practice timer.

## Dataset controls
- 80 encounter rows.
- 151 raw medication-order rows.
- 1 missing unit cost; 1 blank therapeutic class; 1 orphan encounter reference.
- One duplicate-like business record is present under a distinct source order ID; candidate detection is based on a business key and does not auto-delete records.
- Mean supplied length of stay: 3.875 days.
- Supplied synthetic readmission flag: 7/80 (8.75%); not independently validated.
- Total ordered quantity: 3,038; this is not dispensing or administration.
- Synthetic order value: INR 100,279.75; rows with missing cost do not contribute.

## Platform notes
- Full Power Query and Excel desktop feature path is Windows + Microsoft Excel desktop.
- Linux instructions use LibreOffice Calc for compatible spreadsheet work and Python/pandas for ETL; this is not feature-equivalent to Power Query.
- Formula cells are written into the workbook. openpyxl does not calculate formulas; Excel recalculates them when opened.
- Use the local HTTP server; opening index.html via file:// is unsupported for content fetches.
