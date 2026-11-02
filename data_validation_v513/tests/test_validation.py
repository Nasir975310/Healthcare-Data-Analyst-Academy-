import importlib.util,json
from pathlib import Path
SCRIPT=Path(__file__).parents[1]/'scripts/validate_dataset.py'
spec=importlib.util.spec_from_file_location('dq',SCRIPT); dq=importlib.util.module_from_spec(spec); spec.loader.exec_module(dq)
ROOT=Path(__file__).parents[1]
def test_clean_fixture_passes(tmp_path):
 r=dq.validate(ROOT/'data/synthetic_study.csv',ROOT/'config/validation_rules.json',tmp_path,ROOT/'dictionary/core_variables.json')
 assert r['status']=='PASS' and r['rows_checked']==8 and r['error_count']==0
 assert (tmp_path/'validation_report.json').exists() and (tmp_path/'quality_report.html').exists()
def test_duplicate_and_bad_category_are_errors(tmp_path):
 p=tmp_path/'bad.csv'; p.write_text('participant_id,encounter_id,encounter_date,exposure_group\nP1,E1,2026-01-01,exposed\nP2,E1,2026-01-02,unknown\n')
 r=dq.validate(p,ROOT/'config/validation_rules.json',tmp_path/'out')
 assert r['status']=='FAIL' and r['error_count']>=2
def test_temporal_order_rule(tmp_path):
 p=tmp_path/'temporal.csv'; p.write_text('participant_id,encounter_id,index_date,follow_up_end\nP1,T1,2026-03-01,2026-02-01\n')
 r=dq.validate(p,ROOT/'config/validation_rules.json',tmp_path/'out')
 assert any(x['rule_id']=='followup_after_index' for x in r['issues'])
