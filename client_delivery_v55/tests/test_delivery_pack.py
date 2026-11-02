from pathlib import Path
import subprocess,sys,json,zipfile

def test_delivery_pack(tmp_path):
    base=Path(__file__).resolve().parents[1]
    source=base.parent/"report_generator_v54"/"data"/"report_sample.csv"
    result=subprocess.run([sys.executable,str(base/"scripts/build_delivery_pack.py"),"--project","QA demo","--input",str(source),"--output-dir",str(tmp_path)],capture_output=True,text=True,check=True)
    pack=tmp_path/"client_delivery_pack"; manifest=json.loads((pack/"artifact_manifest.json").read_text())
    assert manifest["source_dataset"]["rows"]==120
    assert (pack/"HANDOFF_README.md").is_file() and (pack/"CLIENT_HANDOFF_CHECKLIST.md").is_file()
    with zipfile.ZipFile(tmp_path/"client_delivery_pack.zip") as z: assert z.testzip() is None
