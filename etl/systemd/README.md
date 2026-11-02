# Optional systemd user timer (Linux)

1. Extract Academy to `~/healthcare_data_analyst_academy` or edit `WorkingDirectory` and `ExecStart` paths in the service file.
2. Copy both unit files to `~/.config/systemd/user/`.
3. Run:
```bash
systemctl --user daemon-reload
systemctl --user enable --now hda-etl.timer
systemctl --user list-timers
journalctl --user -u hda-etl.service
```
This is a local training schedule, not a production service. Disable it with:
```bash
systemctl --user disable --now hda-etl.timer
```
