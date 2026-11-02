# Clinical Data Warehouse & Advanced SQL Engineering — v5.26.0

Build a dimensional warehouse from v5.25 FHIR ETL CSV outputs.

1. Run v5.25 ETL to create `outputs/demo`.
2. Run:
```bash
python clinical_data_warehouse_sql_engineering_v526/scripts/build_warehouse.py --input-dir healthcare_data_engineering_interoperability_v525/outputs/demo --output-db clinical_data_warehouse_sql_engineering_v526/outputs/hospital_warehouse.sqlite --cohort-status finished
```
Outputs: SQLite star schema and `warehouse_manifest.json`. SQL examples are in `sql/analytics_examples.sql`. See `docs/warehouse_design.md` for grain, joins and SCD limitations. Synthetic data only.
