$ErrorActionPreference = "Stop"
python -m pip install -e ".[dev]"
if ($LASTEXITCODE -ne 0) { throw "Dependency installation failed" }
python -m pytest -q
if ($LASTEXITCODE -ne 0) { throw "Tests failed" }
python -m health_analytics.profile
if ($LASTEXITCODE -ne 0) { throw "Profiling failed" }
