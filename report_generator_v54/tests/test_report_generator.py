from pathlib import Path
import subprocess,sys,json

def test_generator_creates_docx_pdf_and_manifest(tmp_path):
    base=Path(__file__).resolve().parents[1]
    script=base/"scripts/generate_report.py"
    src=base/"data/report_sample.csv"
    subprocess.run([sys.executable,str(script),"--input",str(src),"--output-dir",str(tmp_path)],check=True,capture_output=True,text=True)
    assert (tmp_path/"healthcare_analytics_report.docx").stat().st_size>1000
    assert (tmp_path/"healthcare_analytics_report.pdf").stat().st_size>1000
    data=json.loads((tmp_path/"report_manifest.json").read_text())
    assert data["rows"]>0 and len(data["sha256"])==64
