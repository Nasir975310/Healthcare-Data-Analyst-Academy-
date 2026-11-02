# Platform guide — Power BI and Linux alternatives

## Windows: primary Power BI route
1. Install Microsoft Power BI Desktop from Microsoft's official download channel or Microsoft Store.
2. Extract the Academy release to a stable folder.
3. Open Power BI Desktop and choose **Get data → Text/CSV**.
4. Import the seven `pbi_*.csv` files in `assignments/data/`.
5. Follow `powerbi/MODEL_RELATIONSHIPS.md` in Model view.
6. Add measures from `powerbi/measures.dax` one at a time using **Modeling → New measure**.
7. Import `powerbi/hda_powerbi_theme.json` through **View → Themes → Browse for themes**.
8. Build the report from `powerbi/REPORT_BLUEPRINT.md`.
9. Save the `.pbix` in your own project folder. The Academy does not generate a PBIX because that requires Power BI Desktop's proprietary authoring engine.

## Linux / CachyOS / Ryoku
Power BI Desktop is not natively supported on Linux. Do not assume Wine or a generic Windows VM will provide a reliable, supported Power BI authoring environment.

### Included Streamlit + Plotly alternative
This is a Linux-friendly way to practise dashboard layout, filters, metrics and data quality. It does not implement DAX, Power Query or PBIX.

From the Academy root, in Fish:
```fish
python -m venv .venv
source .venv/bin/activate.fish
pip install -r requirements-powerbi-linux.txt
streamlit run scripts/powerbi_linux_dashboard.py
```
In Bash:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-powerbi-linux.txt
streamlit run scripts/powerbi_linux_dashboard.py
```
In Windows PowerShell:
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements-powerbi-linux.txt
py -m streamlit run scripts\powerbi_linux_dashboard.py
```
Open the local URL printed by Streamlit (normally `http://localhost:8501`).

### Skill translation
| Power BI skill | Linux practice equivalent | Important difference |
|---|---|---|
| Power Query ETL | pandas transformations | M language and Power Query UI not reproduced |
| DAX measures | pandas calculations | DAX filter context and semantic model not reproduced |
| Model relationships | explicit pandas merges / keys | No Power BI relationship engine |
| Report visuals | Streamlit + Plotly | No PBIX, DAX engine or Power BI service |
| Publishing | local app / separate hosting | Not Power BI Service deployment |

For Power BI job requirements, complete the actual Windows Desktop exercises when access is available. A Linux dashboard is useful portfolio evidence but must be labelled as Streamlit/Plotly, not Power BI.

## Memory and performance
The provided dataset is small. On a 16 GB machine, avoid running a heavy Windows VM alongside browsers, IDEs and containers unless necessary. Close unused workloads before running larger models. Streamlit is a lightweight practice alternative.

## Privacy
Only synthetic data is supplied. Never use real patient identifiers or clinical records in a public dashboard or unapproved cloud service.
