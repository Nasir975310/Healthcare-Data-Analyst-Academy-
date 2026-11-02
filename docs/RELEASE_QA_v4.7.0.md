# v4.7.0 Release QA

## Delivered
- Linux/Ryoku and Windows/PowerShell environment guides.
- Reusable Python project scaffold with pyproject.toml, isolated venv instructions, pytest and Ruff configuration.
- 150-row synthetic encounter dataset and a tested pandas profile script.
- SQLite loader and SQL starter queries.
- Optional PostgreSQL 16 Docker Compose service bound to 127.0.0.1.
- Interactive cross-platform setup checklist, local progress persistence and JSON export.
- Explicit statement that checklist status is self-reported and no computer inspection or installation occurs.

## Executed checks
- `node --check` on the new module.
- Starter project pytest: 1 passed (plugin autoload disabled to avoid unrelated globally installed plugin noise).
- Profile script: 150 rows, 7 columns, zero duplicate encounter IDs; 29 missing discharge dispositions in synthetic fixture.
- SQLite loader: 150 rows loaded; zero duplicate encounter IDs.
- Python syntax and JSON parsing checks.
- Full academy regression tests from earlier releases rerun where relevant.

## Not performed
- Windows execution.
- Docker/PostgreSQL service startup.
- Browser automation or real VS Code GUI testing.
- External security review or production clinical validation.

All included data is synthetic. Do not use real PHI in this training scaffold.
