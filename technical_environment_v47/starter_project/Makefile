PYTHON ?= python
.PHONY: install test lint profile clean
install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e ".[dev]"
test:
	$(PYTHON) -m pytest -q
lint:
	$(PYTHON) -m ruff check src tests
profile:
	$(PYTHON) -m health_analytics.profile
clean:
	$(PYTHON) -c "from pathlib import Path; import shutil; [shutil.rmtree(p) for p in Path('.').rglob('__pycache__') if p.is_dir()]"
