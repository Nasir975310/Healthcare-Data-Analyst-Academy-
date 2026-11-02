from pathlib import Path
import subprocess,sys,json
BASE=Path(__file__).resolve().parents[1]
def test_sample_profile():
    subprocess.run([sys.executable,str(BASE/'scripts/profile_sample.py')],check=True,capture_output=True,text=True)
    x=json.loads((BASE/'output/profile.json').read_text())
    assert x['rows']==60
    assert x['columns']==8
    assert x['duplicate_encounter_ids']==2
    assert len(x['profile'])==8
