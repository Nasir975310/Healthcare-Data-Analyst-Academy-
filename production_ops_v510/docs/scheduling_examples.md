# Scheduling examples (templates; not executed)

## Linux systemd user service
Create `~/.config/systemd/user/healthcare-analytics.service`:
```ini
[Unit]
Description=Healthcare analytics reference pipeline

[Service]
Type=oneshot
WorkingDirectory=%h/healthcare_data_analyst_academy/production_ops_v510
ExecStart=/usr/bin/python scripts/run_pipeline.py
```
Create `~/.config/systemd/user/healthcare-analytics.timer`:
```ini
[Unit]
Description=Run healthcare analytics reference pipeline daily

[Timer]
OnCalendar=*-*-* 06:00:00
Persistent=true

[Install]
WantedBy=timers.target
```
Enable with `systemctl --user daemon-reload`, `systemctl --user enable --now healthcare-analytics.timer`; inspect with `systemctl --user list-timers` and `journalctl --user -u healthcare-analytics.service`.

## Windows Task Scheduler
Program: `py` (or full path to python.exe). Arguments: `scripts\run_pipeline.py`. Start in: the module directory. Configure a service account, retry policy, run history and failure notification. Validate the working directory and Python environment under the scheduled identity.

These are examples, not a claim that a task/timer was created.
