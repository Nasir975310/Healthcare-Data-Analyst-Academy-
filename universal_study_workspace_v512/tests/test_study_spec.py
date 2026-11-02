import importlib.util
from pathlib import Path
SCRIPT=Path(__file__).parents[1]/'scripts/validate_study_spec.py'
spec=importlib.util.spec_from_file_location('validator',SCRIPT); validator=importlib.util.module_from_spec(spec); spec.loader.exec_module(validator)
def valid_spec():
 return {'study_title':'Example cohort study','study_design':'observational_cohort','research_question':'Is exposure associated with later outcome?','population':{'target_population':'Eligible participants','inclusion_criteria':['Eligible'],'exclusion_criteria':[]},'variables':[{'name':'exposure','role':'exposure','data_type':'category','definition':'Baseline exposure group','allowed_values':['yes','no']},{'name':'outcome','role':'outcome','data_type':'boolean','definition':'Outcome during follow-up'}]}
def test_valid_spec_passes():
 result=validator.validate(valid_spec()); assert result['valid'] is True and result['errors']==[]
def test_duplicate_variable_rejected():
 s=valid_spec(); s['variables'].append(dict(s['variables'][0])); result=validator.validate(s)
 assert any(x.startswith('duplicate_variable_name') for x in result['errors'])
def test_missing_inclusion_rejected():
 s=valid_spec(); s['population']['inclusion_criteria']=[]; result=validator.validate(s)
 assert 'inclusion_criteria_required' in result['errors']
