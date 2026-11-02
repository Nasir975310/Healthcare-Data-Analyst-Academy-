from pathlib import Path
import subprocess,sys,json

def test_version_comparison(tmp_path):
    base=Path(__file__).resolve().parents[1]
    src=base.parent/"report_generator_v54"/"data"/"report_sample.csv"
    newer=tmp_path/"new.csv"; newer.write_text(src.read_text()+"")
    out=tmp_path/"compare.json"
    subprocess.run([sys.executable,str(base/"scripts/compare_versions.py"),"--old",str(src),"--new",str(newer),"--output",str(out)],check=True,capture_output=True,text=True)
    result=json.loads(out.read_text())
    assert result["row_delta"]==0 and result["duplicate_row_delta"]==0
