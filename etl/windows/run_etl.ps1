$ErrorActionPreference = "Stop"
$AcademyRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Python = Join-Path $AcademyRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $Python)) { $Python = "py" }
& $Python (Join-Path $AcademyRoot "scripts\healthcare_etl_pipeline.py") --source csv
if ($LASTEXITCODE -ne 0) { throw "Healthcare ETL failed with exit code $LASTEXITCODE" }
