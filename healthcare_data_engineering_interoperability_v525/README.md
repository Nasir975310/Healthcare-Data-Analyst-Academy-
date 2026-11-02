# Healthcare Data Engineering & Clinical Data Interoperability — v5.25.0

Run from the Academy root:

```bash
python healthcare_data_engineering_interoperability_v525/scripts/fhir_analytics_etl.py --input healthcare_data_engineering_interoperability_v525/data/synthetic_hospital_fhir_bundle.json --config healthcare_data_engineering_interoperability_v525/templates/pipeline_config.json --output healthcare_data_engineering_interoperability_v525/outputs/demo
```

Python standard library only. Outputs: resource-level CSVs, patient-encounter longitudinal CSV, SQLite database, validation report, quality report, cohort flow, data dictionary and SHA-256 manifest. See `docs/methods.md` for scope and limitations. Synthetic educational data only.
