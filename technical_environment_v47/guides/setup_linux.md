# Linux setup (Arch/Ryoku, Ubuntu and similar)

From the extracted academy folder:
```bash
cd technical_environment_v47/starter_project
python --version
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m pytest -q
python -m health_analytics.profile
```
Fish activation: `source .venv/bin/activate.fish`. On Arch-based systems, install Python using `sudo pacman -S --needed python python-pip`. Keep dependencies inside the venv; do not use `sudo pip`.

## VS Code
Open `starter_project`, install Python and Jupyter extensions, select `.venv/bin/python`, then run `python -m pytest -q` in the integrated terminal.

## Optional PostgreSQL
With Docker running: `docker compose up -d`, `docker compose ps`, then `docker compose down`. PostgreSQL binds to localhost only. The password is a disposable local training value; change it before any real use.

## Troubleshooting
- `python` missing: install Python 3.10+ using your distribution package manager.
- `ensurepip` missing: install your distribution's venv/pip support.
- Permission errors: use a user-owned directory and venv, never `sudo pip`.
- VS Code import errors: reselect `.venv/bin/python`.
- Docker daemon unavailable: start Docker before compose.
