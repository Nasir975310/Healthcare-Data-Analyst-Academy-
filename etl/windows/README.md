# Windows PowerShell scheduling

From PowerShell:
```powershell
cd C:\path\to\healthcare_data_analyst_academy
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements-etl.txt
powershell -ExecutionPolicy Bypass -File .\etl\windows\run_etl.ps1
```

To schedule daily at 06:30 (adjust the path):
```powershell
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument '-NoProfile -ExecutionPolicy Bypass -File "C:\path\to\healthcare_data_analyst_academy\etl\windows\run_etl.ps1"'
$trigger = New-ScheduledTaskTrigger -Daily -At 6:30AM
Register-ScheduledTask -TaskName "HDA-Synthetic-ETL" -Action $action -Trigger $trigger -Description "Local synthetic healthcare ETL training"
```
Inspect with `Get-ScheduledTask -TaskName HDA-Synthetic-ETL`. Remove with `Unregister-ScheduledTask -TaskName HDA-Synthetic-ETL`.
