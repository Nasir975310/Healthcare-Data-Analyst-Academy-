# Healthcare Data Analyst Academy (HDA Academy)

[![Academy Quality Checks](https://github.com/Nasir975310/Healthcare-Data-Analyst-Academy-/actions/workflows/quality.yml/badge.svg)](https://github.com/Nasir975310/Healthcare-Data-Analyst-Academy-/actions/workflows/quality.yml)
[![Version](https://img.shields.io/badge/Release-v5.60.3-blue.svg)](RELEASE_NOTES_v5.60.3.md)
[![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-success.svg)](requirements-dev.txt)
[![Tests Passed](https://img.shields.io/badge/Tests-68%2F68%20Passed-brightgreen.svg)](FULL_TEST_REPORT.json)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Offline First](https://img.shields.io/badge/Architecture-Offline--First-teal.svg)](#interactive-learning-portal)

An enterprise-grade, offline-first learning platform, data laboratory, and career portfolio system designed for healthcare data analysts, health informaticians, and clinical data engineers.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Interactive Learning Portal](#-interactive-learning-portal)
- [Curriculum & Architecture](#-curriculum--architecture)
- [Quick Start](#-quick-start)
- [ETL & Data Engineering Pipeline](#-etl--data-engineering-pipeline)
- [Testing & Quality Verification](#-testing--quality-verification)
- [Repository Structure](#-repository-structure)
- [Data Integrity & Governance](#-data-integrity--governance)
- [Documentation Library](#-documentation-library)
- [Contributing & License](#-contributing--license)

---

## 🏥 Overview

The **Healthcare Data Analyst Academy** bridges the gap between academic clinical informatics and real-world healthcare analytics engineering. It provides a complete, structured ecosystem covering:

1. **Healthcare Data Warehousing:** Relational schema design, dimensional modeling (Star/Snowflake), clinical data contracts, and ETL pipelines.
2. **Clinical Biostatistics & Epidemiology:** Observational cohort studies, Drug Utilization Evaluation (DUE), propensity scoring, logistic regression, and survival analysis.
3. **Data Quality & Governance:** Automated quarantine frameworks, orphan order detection, PHI redaction, and metric reconciliation.
4. **Business Intelligence & Visual Analytics:** Executive stakeholder reports, Power BI data models, Streamlit dashboards, and reproducible figures.
5. **Career Launch & Portfolio Engineering:** Automated evidence capture, verifiable test-driven portfolio projects, vacancy match analysis, and interview simulations.

---

## 🌐 Interactive Learning Portal

The repository includes a responsive, zero-external-dependency web application ([`index.html`](index.html)) with 70+ interactive modules:

- **Volume Reader & Progress Tracker:** Step-by-step curriculum with client-side localStorage persistence and JSON export/import.
- **Embedded Statistical Calculators:** Interactive calculators for Bayesian diagnostic accuracy (Sensitivity, Specificity, PPV, NPV), descriptive statistics (Mean, Median, IQR, SD), and normal confidence intervals.
- **Mastery Laboratories:** Challenge banks for Excel, PostgreSQL, Health Data Engineering, Power BI, and Epidemiology.
- **Offline First:** Self-contained static architecture that functions without internet connectivity or external CDN dependencies.

### Launching the Portal

Launch the local web server from the repository root:

```bash
python3 -m http.server 8000
```

Open your browser to: **[http://localhost:8000/index.html](http://localhost:8000/index.html)**

---

## 📚 Curriculum & Architecture

The curriculum is structured across eight core volumes and five operational pillars:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   HEALTHCARE DATA ANALYST ACADEMY                      │
└────────────────────────────────────────────────────────────────────────┘
        │
        ├── 01. Foundations: Data Literacy, Healthcare Vocabularies & Stats
        ├── 02. Spreadsheet & Database Mastery: Excel Formulas, Power Query & SQL
        ├── 03. Reproducible Analytics: Python, Pandas, Matplotlib & Scripting
        ├── 04. Clinical Research: DUE Studies, Epidemiology & Hypothesis Testing
        ├── 05. BI & Warehousing: PostgreSQL, Dimensional Schemas & Dashboards
        ├── 06. Data Engineering: Automated ETL, Data Contracts & Idempotency
        ├── 07. Advanced Specialization: Interoperability (HL7/FHIR) & Quality Ops
        └── 08. Professional Practicum: Client Simulations, Review Gates & Career
```

---

## ⚡ Quick Start

### 1. Prerequisites

- Python 3.10+ (tested on Python 3.11, 3.12, 3.13, and 3.14)
- Git

### 2. Environment Setup

Using [`uv`](https://github.com/astral-sh/uv) (recommended for blazing-fast setup):

```bash
# Clone the repository
git clone https://github.com/Nasir975310/Healthcare-Data-Analyst-Academy-.git
cd Healthcare-Data-Analyst-Academy-

# Create virtual environment and install development dependencies
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements-dev.txt
```

Or using standard `python3`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

---

## 🔄 ETL & Data Engineering Pipeline

The Academy features production-grade healthcare data pipelines with schema validation, record quarantining, and execution manifests.

Run the end-to-end hospital encounters and medication orders ETL pipeline:

```bash
bash scripts/run_healthcare_etl.sh
```

**Pipeline features:**
- Source data profiling and data contract validation.
- Automated quarantine of corrupt or unmapped encounter identifiers.
- Curates SQLite/PostgreSQL analytical tables (`encounters`, `medication_orders`).
- Generates JSON execution audit manifests with record counts and timestamped hashes.

---

## ✅ Testing & Quality Verification

All suites in this repository adhere to rigorous acceptance and reproducibility standards:

### 1. Maintained Career Release Suites

Runs the 6 primary career-gate validation suites via pytest:

```bash
pytest -q
```
*Expected: 36 passed tests across 6 suites.*

### 2. Full Academy Test Audit

Inventories and executes all 68 isolated module test directories across the entire repository:

```bash
python scripts/verify_full_academy.py --jobs 4 --timeout 30
```
*Expected: 68 / 68 suites passed (writes [`FULL_TEST_REPORT.json`](FULL_TEST_REPORT.json)).*

### 3. Release Quality & Integrity Checks

```bash
# Verify Python syntax (AST parsing across all files)
python scripts/verify_release.py

# Validate release documentation and version headers
python scripts/validate_release_docs.py

# Verify local link resolution in web entry points
python scripts/verify_local_links.py

# Scan for accidental sensitive patterns or secrets
python scripts/scan_sensitive_patterns.py
```

---

## 📂 Repository Structure

```
Healthcare-Data-Analyst-Academy-/
├── index.html                  # Core interactive web platform UI
├── ROADMAP.html                # Visual interactive learning roadmap
├── assets/                     # Styles, core app engine (app.js), icons
│   ├── app.js                  # Client-side routing, calculators & state
│   ├── styles.css              # Modern responsive styling & themes
│   └── favicon.svg             # Vector branding icon
├── scripts/                    # Maintenance, ETL pipelines & audit runners
│   ├── healthcare_etl_pipeline.py  # Production hospital ETL runner
│   ├── run_healthcare_etl.sh       # Shell orchestration wrapper
│   ├── verify_full_academy.py      # Independent test suite runner
│   ├── verify_release.py           # Core acceptance & AST parser
│   └── verify_local_links.py       # Static link integrity checker
├── content/                    # Curriculum JSON data, glossaries, challenges
├── assignments/                # Job simulation briefs, scoring rubrics & data
├── projects/                   # Capstones (Biostatistics, Pharmacy, Portfolios)
├── advanced_sql/               # Complex query challenge bank
├── clinical_research/          # Study protocols, cohorts & analysis code
├── powerbi/                    # DAX measures, data models & PBI specifications
├── postgresql/                 # DDL, partitioning, views & procedures
├── requirements-dev.txt        # Consolidated development requirements
└── .github/workflows/          # Continuous Integration workflow (quality.yml)
```

---

## 🔒 Data Integrity & Governance

- **Synthetic Training Data:** All hospital records, patient encounters, laboratory observations, and medication orders utilized in exercises and automated tests are **100% synthetic and fictional**. They do not represent real individuals or institutions.
- **Academic Distinction:** The real Pharm.D thesis (*Drug Utilization Evaluation of Antihypertensives in a Tertiary Care Teaching Hospital*, prospective observational, N=153) is maintained as a distinct methodological reference and is never merged with synthetic training data.
- **Privacy Policy:** Never commit Protected Health Information (PHI), patient identifiers, private tokens, or institution-restricted credentials. See [`DATA_HANDLING_POLICY.md`](DATA_HANDLING_POLICY.md) and [`SECURITY.md`](SECURITY.md).

---

## 📖 Documentation Library

- [**GETTING_STARTED.md**](GETTING_STARTED.md) — Comprehensive onboarding guide for new analysts.
- [**LEARNING_PATHS.md**](LEARNING_PATHS.md) — Recommended tracks (Beginner, SQL/BI Specialist, Python Data Engineer).
- [**ACADEMY_CATALOG.md**](ACADEMY_CATALOG.md) — Exhaustive catalog of all course-packs and practical modules.
- [**SHOWCASE.md**](SHOWCASE.md) — Portfolio-ready deliverables and case studies.
- [**STABILIZATION_REPORT.md**](STABILIZATION_REPORT.md) — Quality metrics and engineering audit summary.
- [**MODULE_COMPATIBILITY_MATRIX.md**](MODULE_COMPATIBILITY_MATRIX.md) — Dependencies and tooling compatibility across modules.

---

## 🤝 Contributing & License

Contributions, issue reports, and curriculum enhancements are welcome! Please review [**CONTRIBUTING.md**](CONTRIBUTING.md) for contribution guidelines and testing requirements.

Distributed under the **MIT License**. See [**LICENSE**](LICENSE) for details.
