import argparse, json, re
from pathlib import Path

SKILL_TERMS={
 'sql':['sql','sqlite','postgresql','joins','aggregation'],
 'python':['python','pandas','data cleaning','data validation'],
 'excel':['excel','spreadsheet','pivot table'],
 'power bi':['power bi','dax','power query','dashboard'],
 'healthcare_domain':['healthcare','clinical','pharmacy','pharm.d','pharmacovigilance'],
 'communication':['communication','stakeholder','documentation','reporting'],
 'privacy':['privacy','confidential','patient data','data protection']
}
LEVELS={'demonstrated':1.0,'practised':0.65,'learning':0.3,'not held':0.0}

def evaluate(job_text,evidence):
    job=job_text.lower()
    found=[skill for skill,terms in SKILL_TERMS.items() if any(term in job for term in terms)]
    skills=evidence.get('skills',{})
    detail=[]
    for skill in found:
        item=skills.get(skill,{})
        level=item.get('level','not held').lower()
        detail.append({'skill':skill,'level':level,'weight':LEVELS.get(level,0.0),
                       'evidence':item.get('evidence',[]),'limitations':item.get('limitations',[])})
    score=round(sum(x['weight'] for x in detail)/len(detail)*100) if detail else 0
    return {'matched_skill_categories':len(found),'evidence_fit_percent':score,'details':detail,
            'interpretation':'Heuristic keyword/evidence fit only; not an ATS score, probability of interview or hiring recommendation.',
            'next_step':'Tailor only demonstrated/practised skills honestly; identify gaps and confirm mandatory criteria manually.'}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--job',required=True);p.add_argument('--evidence',required=True)
    a=p.parse_args()
    result=evaluate(Path(a.job).read_text(encoding='utf-8'),json.loads(Path(a.evidence).read_text(encoding='utf-8')))
    print(json.dumps(result,indent=2))
