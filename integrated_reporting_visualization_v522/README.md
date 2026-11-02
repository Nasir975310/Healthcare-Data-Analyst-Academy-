# Integrated Reporting & Visualization Engine v5.22.0

A configuration-driven local Python pipeline connecting descriptive statistical outputs to publication-style tables, figures, reports and a hashed evidence manifest.

## Install and run

```bash
python -m pip install -r integrated_reporting_visualization_v522/requirements.txt
python integrated_reporting_visualization_v522/scripts/integrated_reporting.py \
  --input integrated_reporting_visualization_v522/data/synthetic_reporting_dataset.csv \
  --config integrated_reporting_visualization_v522/templates/report_config.json \
  --output integrated_reporting_visualization_v522/outputs/demo
```

Run from the Academy root. For custom data, copy the JSON config and update its column names and relative effect-file paths. Supported input: CSV, XLSX/XLS, Parquet. The forest and coefficient CSV files require the columns documented in the template's example data.

## Outputs

- `table1.csv`
- `figures/*.png` (300 dpi)
- `roc_summary.json`, `kaplan_meier_summary.json` when configured
- `executive_summary.md`, `technical_report.md`
- `report_config.json` (configuration snapshot)
- `evidence_manifest.json` (input and output SHA-256, sizes, validation)

## Integration

This release reuses the conceptual output formats and methods of v5.16 visualization and v5.17 publication workbench, but is a unified orchestrator with its own config and CLI. It does not silently modify prior modules or execute their scripts as hidden subprocesses. Outputs can be copied into the v5.17 publication workbench for further manuscript assembly.

## Statistical cautions

ROC is apparent only and not validated. Kaplan–Meier is descriptive only. Forest plot is display-only and performs no pooling. Table 1 is descriptive and does not imply baseline comparability. No automatic assumption checks, missing-data imputation, multiplicity correction, causal inference or external validation is performed. Do not use for treatment decisions. Use only appropriately governed, de-identified data in real workflows; never place identifiable patient data in portfolio outputs.

## Export to v5.17 publication workbench
After generating the report, run this from the Academy root to create a new, non-overwriting handoff folder:

```bash
python integrated_reporting_visualization_v522/scripts/export_to_publication_workbench.py --source integrated_reporting_visualization_v522/outputs/demo --destination research_publication_workbench_v517/outputs/v522_handoff
```

The exporter refuses to overwrite a non-empty destination. It copies the Table 1, reports, config, evidence manifest and figures, then creates a separate handoff hash manifest.
