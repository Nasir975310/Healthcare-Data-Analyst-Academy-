#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="${ROOT}/.venv/bin/python"
if [[ ! -x "$PYTHON" ]]; then PYTHON="python3"; fi
"$PYTHON" "${ROOT}/scripts/healthcare_etl_pipeline.py" --source csv
