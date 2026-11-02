# V06 BI and data engineering capstone

## Purpose
Build a small, reproducible BI data mart from synthetic patient, encounter and medication-order data. It demonstrates dimensional grain, ETL validation, aggregation, metric definitions and a Linux-friendly execution path.

## Run locally
From this project folder:
```bash
python -m pip install -r requirements.txt
python python/build_marts.py
```

## Run with Docker
```bash
docker build -t healthcare-bi-capstone .
docker run --rm healthcare-bi-capstone
```

## Power BI and Linux
Power BI Desktop is a Windows desktop product and is not natively supported on CachyOS/Ryoku Linux. This project provides portable CSV marts and SQL definitions that can be imported into Power BI from an authorised Windows environment. For local Linux dashboard practice, use a supported browser-based BI deployment such as Metabase or Apache Superset after reviewing its installation, security and resource requirements. A browser-hosted Power BI Service account does not necessarily provide the full Desktop modelling workflow.

## Data caution
All rows are synthetic. The readmission flag is generated for teaching and is not a validated hospital readmission measure. No clinical, quality or causal conclusion is supported.
