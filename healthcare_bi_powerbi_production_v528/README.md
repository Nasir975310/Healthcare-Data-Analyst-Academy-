# v5.28.0 — Healthcare BI & Power BI Production Engineering

A synthetic end-to-end BI modelling project covering Power Query, DAX, star schema, KPI definitions, RLS design, data quality and performance practices.

## Run source QA
**Ryoku / Arch Linux:** `python -m venv .venv && source .venv/bin/activate && python -m unittest discover -s tests -v && python scripts/validate_sources.py`

**Windows PowerShell:** `py -m venv .venv; .\.venv\Scripts\Activate.ps1; python -m unittest discover -s tests -v; python scripts/validate_sources.py`

Open `docs/implementation_guide.md` for the Power BI build procedure. Dataset is fictional and contains no real patient records. M/DAX files are templates, not executed artifacts.
