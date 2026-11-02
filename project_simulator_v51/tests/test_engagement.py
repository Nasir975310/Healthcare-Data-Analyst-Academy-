from pathlib import Path
import json, subprocess, sys
BASE=Path(__file__).resolve().parents[1]
def test_pipeline_reconciles_and_outputs():
    subprocess.run([sys.executable,str(BASE/'scripts/run_engagement.py')],check=True,capture_output=True,text=True)
    s=json.loads((BASE/'output/engagement_summary.json').read_text())
    assert s['raw_rows']==120
    assert s['raw_rows']==s['accepted_rows']+s['quarantined_rows']
    assert s['accepted_encounters_unique'] is True
    assert s['quarantined_rows']>0
    assert s['average_los_discharged_calendar_days'] is not None
