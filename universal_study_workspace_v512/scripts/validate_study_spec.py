#!/usr/bin/env python3
"""Validate structure and basic consistency of an exported study specification."""
from pathlib import Path
import argparse,json,re,sys
ROOT=Path(__file__).resolve().parents[1]
DESIGNS=json.loads((ROOT/'templates/study_designs.json').read_text())
ROLES={'exposure','comparator','outcome','covariate','demographic','process','safety','identifier','other'}
TYPES={'integer','decimal','string','date','datetime','boolean','category'}
def validate(spec):
    errors=[]; warnings=[]
    for key in ('study_title','study_design','research_question','population','variables'):
        if key not in spec: errors.append('missing_required_field:'+key)
    design=spec.get('study_design')
    if design not in DESIGNS: errors.append('unknown_study_design')
    if not isinstance(spec.get('study_title'),str) or len(spec.get('study_title','').strip())<3: errors.append('invalid_study_title')
    if not isinstance(spec.get('research_question'),str) or len(spec.get('research_question','').strip())<10: errors.append('research_question_too_short')
    pop=spec.get('population',{})
    if not isinstance(pop,dict): errors.append('population_must_be_object'); pop={}
    for key in ('target_population','inclusion_criteria','exclusion_criteria'):
        if key not in pop: errors.append('population_missing:'+key)
    if not isinstance(pop.get('inclusion_criteria',[]),list) or not pop.get('inclusion_criteria'): errors.append('inclusion_criteria_required')
    variables=spec.get('variables',[])
    if not isinstance(variables,list) or not variables: errors.append('variables_must_be_nonempty_array'); variables=[]
    names=set()
    for n,v in enumerate(variables,1):
        if not isinstance(v,dict): errors.append(f'variable_{n}_must_be_object'); continue
        name=v.get('name','')
        if not isinstance(name,str) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*',name): errors.append(f'variable_{n}_invalid_name')
        elif name.lower() in names: errors.append('duplicate_variable_name:'+name)
        else: names.add(name.lower())
        if v.get('role') not in ROLES: errors.append(f'variable_{n}_invalid_role')
        if v.get('data_type') not in TYPES: errors.append(f'variable_{n}_invalid_data_type')
        if not isinstance(v.get('definition'),str) or len(v.get('definition','').strip())<5: errors.append(f'variable_{n}_definition_too_short')
        if v.get('data_type')=='category' and not v.get('allowed_values'): warnings.append(f'variable_{n}_category_without_allowed_values')
        if v.get('role')=='identifier': warnings.append(f'variable_{n}_identifier_privacy_review_required')
    if design in DESIGNS and isinstance(spec.get('time',{}),dict):
        roles={v.get('role') for v in variables if isinstance(v,dict)}
        role_fields={'exposure':'exposure','comparator':'comparator','outcome':'outcome',
                     'primary_outcome':'outcome','confounders':'covariate'}
        aliases={'population':'target_population','index_date':'index_date','follow_up':'follow_up'}
        for field in DESIGNS[design]['required']:
            if field in role_fields and role_fields[field] in roles: continue
            if field in aliases:
                if field=='population' and pop.get('target_population'): continue
                if field in ('index_date','follow_up') and spec.get('time',{}).get(aliases[field]): continue
            if field not in spec and field not in spec.get('time',{}):
                warnings.append('design_specific_field_to_confirm:'+field)
    return {'valid':not errors,'errors':errors,'warnings':warnings,'variable_count':len(variables),'study_design':design}
def main():
    p=argparse.ArgumentParser(); p.add_argument('spec',type=Path); p.add_argument('--output',type=Path)
    a=p.parse_args(); result=validate(json.loads(a.spec.read_text()))
    out=json.dumps(result,indent=2); print(out)
    if a.output: a.output.write_text(out)
    return 0 if result['valid'] else 1
if __name__=='__main__': sys.exit(main())
