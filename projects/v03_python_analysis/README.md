# Volume 3 Python analysis practicals

Run scripts from the academy root, using the virtual environment described in the main README.

```bash
python projects/v03_python_analysis/pandas_fundamentals.py
python projects/v03_python_analysis/data_quality_pipeline.py
python projects/v03_python_analysis/visualize_healthcare_data.py
python projects/v03_python_analysis/statistical_analysis_demo.py
```

The visualization script writes four PNG files to `projects/v03_python_analysis/reports/`. The pandas script writes a department summary CSV. The data-quality script writes a JSON report and row-level flags. The statistical script prints descriptive summaries, a Welch comparison and an exploratory OLS model.

Install dependencies in the active virtual environment:

```bash
python -m pip install pandas numpy matplotlib scipy statsmodels
```

R script: `r_foundations_analysis.R`. Run it from the academy root in R/RStudio. It uses base R only.

All data is fictional. Statistical outputs are demonstrations, not clinical findings. Repeated encounters may belong to the same synthetic patient, so independence assumptions require scrutiny.
