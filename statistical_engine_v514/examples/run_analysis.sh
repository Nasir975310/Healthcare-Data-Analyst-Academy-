#!/usr/bin/env bash
set -euo pipefail
python -m pip install -r requirements.txt
python scripts/analyze_study.py \
  --input data/synthetic_bp_study.csv \
  --outdir outputs \
  --outcome followup_sbp --baseline baseline_sbp \
  --group group --reference intervention --comparison usual_care
