from pathlib import Path
import subprocess,sys,json

def test_quality_audit_outputs(tmp_path):
    base=Path(__file__).resolve().parents[1]
    source=base.parent/"report_generator_v54"/"data"/"report_sample.csv"
    subprocess.run([sys.executable,str(base/"scripts/quality_audit.py"),"--input",str(source),"--output-dir",str(tmp_path)],check=True,capture_output=True,text=True)
    score=json.loads((tmp_path/"quality_scorecard.json").read_text())
    rules=json.loads((tmp_path/"rule_results.json").read_text())
    assert len(rules)==6 and score["score_percent"]<=100
    assert (tmp_path/"issue_register.csv").is_file() and (tmp_path/"audit_manifest.json").is_file()
