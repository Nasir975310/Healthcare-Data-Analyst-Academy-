import json, subprocess, sys
from pathlib import Path
def test_semantic_validation(tmp_path):
    script=Path(__file__).parents[1]/"scripts/run_semantic_validation.py"
    out=tmp_path/"result.json"
    p=subprocess.run([sys.executable,str(script),"--output",str(out)],
      cwd=script.parents[1],capture_output=True,text=True)
    assert p.returncode==0,p.stderr
    data=json.loads(out.read_text())
    assert data["status"]=="PASS"
    assert data["fixture_rows"]==20
    assert data["semantic_rows"]==20
