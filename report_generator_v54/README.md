# v5.4.0 — Healthcare Analytics Report Generator

A local-first report drafting and export module for synthetic or appropriately de-identified CSV data.

## Browser module
Open the Academy `index.html`, select **Report generator v5.4**, load the included sample or your permitted CSV, complete project metadata and methods, then preview/export a standalone HTML report. Use the browser's Print → Save as PDF for a print-ready PDF. The browser module does not generate DOCX files.

## DOCX/PDF generation with Python
From this folder:

### Linux (Ryoku / Arch, Fish or Bash)
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/generate_report.py --input data/report_sample.csv --output-dir output --title "Hospital operations descriptive report"
```

### Windows PowerShell
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py scripts\generate_report.py --input data\report_sample.csv --output-dir output --title "Hospital operations descriptive report"
```

The script creates a DOCX and PDF with dataset profile, summary statistics, methods, data-quality notes and limitations. Review and edit the report before external use.

## Data governance
- The included CSV is synthetic. Never upload identifiable patient data to a public portfolio.
- Confirm lawful basis, minimum necessary fields, de-identification, access controls and institutional policy before using real data.
- This is descriptive reporting support, not clinical decision support or clinical validation.
- No causal inference is performed. Association or descriptive summaries must not be interpreted as treatment effects.
