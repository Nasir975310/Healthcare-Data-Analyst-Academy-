# Optional scheduling examples

## Linux systemd user timer
Create `~/.config/systemd/user/healthcare-etl.service`:
```ini
[Unit]
Description=Healthcare synthetic ETL pipeline

[Service]
Type=oneshot
WorkingDirectory=%h/healthcare_data_analyst_academy/etl_orchestration_v57
ExecStart=%h/healthcare_data_analyst_academy/etl_orchestration_v57/.venv/bin/python scripts/run_pipeline.py --input examples/encounters.csv --config config/pipeline.json --output-dir output
```
Create `~/.config/systemd/user/healthcare-etl.timer`:
```ini
[Unit]
Description=Run healthcare ETL daily

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```
Enable with `systemctl --user daemon-reload && systemctl --user enable --now healthcare-etl.timer`. Adjust paths first.

## Windows Task Scheduler
Create a task that runs `py` with arguments:
`etl_orchestration_v57\scriptsun_pipeline.py --input etl_orchestration_v57\examples\encounters.csv --config etl_orchestration_v57\config\pipeline.json --output-dir etl_orchestration_v57\output`
Set the task's **Start in** directory to the `etl_orchestration_v57` folder. Use an approved account and protect output files.
