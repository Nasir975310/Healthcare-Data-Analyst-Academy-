# Windows setup (PowerShell)

Install Python 3.10+ and VS Code. In PowerShell:
```powershell
Set-Location technical_environment_v47/starter_project
py --version
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m pytest -q
python -m health_analytics.profile
```
If activation is blocked, allow it only for this PowerShell process:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```
Or use `.\.venv\Scripts\python.exe` explicitly without activation.

## VS Code
Open `starter_project`, install Python and Jupyter extensions, then select `.venv\Scripts\python.exe` through **Python: Select Interpreter**.

## Optional PostgreSQL
Install Docker Desktop and start its engine, then run `docker compose up -d`, `docker compose ps`, and `docker compose down`. The service binds to localhost only. Change the sample password before real use.

## Troubleshooting
- `py` missing: install Python and reopen PowerShell.
- Activation blocked: use process-scoped policy above or invoke the venv executable directly.
- VS Code cannot import modules: select the project venv interpreter.
- Docker daemon unavailable: start Docker Desktop.
