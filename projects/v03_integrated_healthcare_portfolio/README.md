# Integrated Healthcare Analytics Portfolio

This project combines Python, R, SQL and reproducible reporting using only the Academy's synthetic hospital encounter data.

## Folder map
- `automation/healthcare_pipeline.py` — command-line Python pipeline.
- `automation/test_pipeline.py` — seven unit tests.
- `r_analysis.R` — independent R summary.
- `r_visualizations.R` — optional ggplot2 charts.
- `sql_reference_capstone_queries.sql` — SQL reference queries from Volume 2.
- `healthcare_analytics_report.qmd` — Quarto report source.
- `reports/` — generated summaries and run metadata.
- `figures/` — figures created by the R visualization script.
- `requirements.txt` — Python dependencies.
- `PROJECT_BRIEF.md` — assignment, definitions and acceptance criteria.

## Setup (Fish shell on Arch-based Linux)
From the Academy root:

```bash
python -m venv projects/v03_integrated_healthcare_portfolio/.venv
```

Activate:

```fish
source projects/v03_integrated_healthcare_portfolio/.venv/bin/activate.fish
```

Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r projects/v03_integrated_healthcare_portfolio/requirements.txt
```

Select this environment in VS Code. Do not use `sudo pip` or modify system-managed Python packages.

## Run the pipeline
From the Academy root:

```bash
python projects/v03_integrated_healthcare_portfolio/automation/healthcare_pipeline.py \
  --input datasets/v03_python/encounters.csv \
  --output-dir projects/v03_integrated_healthcare_portfolio/reports/python_run \
  --start-date 2026-01-01 \
  --end-date 2026-04-01
```

Expected high-level results for the supplied dataset:
- 104 eligible encounters
- 60 distinct synthetic patients
- 96 nonmissing SBP values
- 8 missing SBP values
- 0 unmatched department keys
- Department encounter totals reconcile to 104

## Run automated tests

```bash
python -m unittest discover \
  -s projects/v03_integrated_healthcare_portfolio/automation \
  -p 'test_*.py' -v
```

Seven tests cover unique keys, duplicate rejection, half-open date boundaries, invalid date ranges, missing SBP preservation, department reconciliation and duplicate lookup rejection.

## Run the R implementation
Install R and the packages `readr`, `dplyr` and `ggplot2` in an approved R environment. Open the Academy root as an RStudio Project, then run:

```r
source("projects/v03_integrated_healthcare_portfolio/r_analysis.R")
source("projects/v03_integrated_healthcare_portfolio/r_visualizations.R")
```

The dplyr join script uses relationship validation available in modern dplyr versions. The R scripts were authored but not executed in the release-generation environment because Rscript was unavailable there.

## Render the Quarto report
Install the Quarto CLI and a Python kernel in this project environment. From the Academy root:

```bash
quarto render projects/v03_integrated_healthcare_portfolio/healthcare_analytics_report.qmd
```

Inspect the generated HTML. Rendering has not been tested in the release environment; the `.qmd` is supplied as a complete learner report source.

## Reproducibility and limitations
Record software versions, execution date, source files, reporting window and code revision. The records are synthetic. Descriptive department comparisons are not rankings, clinical benchmarks or causal evidence. Repeated encounters may belong to one patient; inferential analysis must account for clustering where relevant.
