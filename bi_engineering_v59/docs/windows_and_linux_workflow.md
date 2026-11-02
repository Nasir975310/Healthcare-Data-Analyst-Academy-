# Workstation workflow

## Windows / Power BI Desktop
Power BI Desktop is a Windows desktop application. Import the CSV fixture, construct the model using `semantic_model.md`, and paste measures from `powerbi/measures.dax`. Power Query Editor can use `powerquery/transform_encounters.m`; update the file path to the actual local location.

## Linux / Ryoku
Power BI Desktop is not a native Linux application. Use the local Python/SQLite validation lab here and practise DAX/M through the supplied source files. For Power BI Desktop, use a supported Windows installation or managed Windows environment; do not assume Wine provides a supported or reliable Power BI environment.

## Execute local validation
From this module directory:
`python scripts/run_semantic_validation.py`
Windows PowerShell:
`py scripts/run_semantic_validation.py`

The script uses Python's standard library and an in-memory SQLite database. It does not execute DAX or Power Query M.
