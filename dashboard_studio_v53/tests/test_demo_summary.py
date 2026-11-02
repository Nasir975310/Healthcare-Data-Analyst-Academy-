from pathlib import Path
import subprocess,sys,json
BASE=Path(__file__).resolve().parents[1]
def test_demo_summary():
    subprocess.run([sys.executable,str(BASE/'scripts/build_demo_summary.py')],check=True,capture_output=True,text=True)
    x=json.loads((BASE/'output/demo_summary.json').read_text())
    assert x['rows']==120
    assert x['unique_patients']<=120
    assert sum(x['departments'].values())==120
    assert x['sbp_completeness_pct']>0
