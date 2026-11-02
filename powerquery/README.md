# Power Query laboratory

## Windows / Microsoft Excel Desktop
1. Extract the Academy folder to a stable local path.
2. Open `assignments/starter/healthcare_excel_powerquery_lab.xlsx`.
3. Use **Data → Get Data → From Text/CSV** for the three CSV files in `assignments/data/`.
4. Load each as a connection/table. Keep the source queries unchanged.
5. Open `powerquery/clean_orders.m` in a text editor and adapt the file path/query names before using Advanced Editor.
6. Build quality flags and a cleaned output query; load it to a new worksheet/table.
7. Refresh queries and PivotTables after changing source files.

The supplied M file is a teaching pattern, not a ready-to-run workbook query. The path is an example and must be changed. It expects an Excel table named `tblEncounters` in the current workbook. Power Query Desktop execution was not available during QA.

## Linux / LibreOffice
LibreOffice Calc can perform formulas, filters, PivotTables and charts, but its data import/ETL interface is not equivalent to Excel Power Query. Use the supplied Python/pandas alternative:
```bash
python -m venv .venv
source .venv/bin/activate
pip install pandas
python scripts/excel_lab_cleaning.py
```
On Fish shell:
```fish
python -m venv .venv
source .venv/bin/activate.fish
pip install pandas
python scripts/excel_lab_cleaning.py
```
Windows PowerShell:
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install pandas
py scripts\excel_lab_cleaning.py
```

## Data safety
All records are synthetic. Never substitute identifiable patient data or upload PHI to an unapproved service.
