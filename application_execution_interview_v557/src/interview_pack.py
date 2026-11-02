"""Deterministic vacancy-specific interview preparation pack generator."""
import argparse, json, re
from pathlib import Path
from datetime import date
TOPICS={
'SQL':['sql','postgresql','mysql','sqlite'], 'Python':['python','pandas','numpy'],
'Excel':['excel','pivot table','power query'], 'Power BI':['power bi','dax','powerbi'],
'Statistics':['statistics','hypothesis testing','regression','confidence interval'],
'Healthcare':['healthcare','clinical','hospital','patient','pharmacy','pharmacovigilance'],
'Research':['clinical research','observational study','research','study design'],
'Communication':['stakeholder','communication','presentation','reporting'],
'Data quality':['data quality','validation','cleaning','missing data','deduplication']}
QUESTIONS={
'SQL':['How would you identify duplicate encounters without deleting valid repeat visits?','Explain INNER JOIN versus LEFT JOIN with a healthcare example.','How would you reconcile a SQL report to its source table?'],
'Python':['Describe a reproducible pandas data-cleaning workflow.','How would you handle missing, duplicated and out-of-range values?','How would you make an analysis script reproducible?'],
'Excel':['How would you use PivotTables to summarise service utilisation?','How would you audit spreadsheet formulas?'],
'Power BI':['How would you design a dashboard for healthcare KPIs?','Explain a measure versus a calculated column.'],
'Statistics':['When would you use a paired t-test?','How do statistical and clinical significance differ?','What assumptions would you check before ANOVA?'],
'Healthcare':['How does Pharm.D training help interpret healthcare data?','What privacy principles govern patient-level data access?'],
'Research':['Describe your prospective observational antihypertensive utilisation thesis and its limitations.','How do you distinguish association from causation?'],
'Communication':['How would you explain a data-quality limitation to a clinical stakeholder?','How do you decide what belongs in an executive summary?'],
'Data quality':['Describe validation before calculating KPIs.','How would you document exclusions for reproducibility?']}
def make_pack(jd,profile,title='Unspecified role'):
    if not jd.strip(): raise ValueError('Job description is empty.')
    low=jd.lower(); detected=[k for k,v in TOPICS.items() if any(t in low for t in v)]
    skills={x.lower() for x in profile.get('skills',[])}
    matched=[x for x in detected if x.lower() in skills]; gaps=[x for x in detected if x.lower() not in skills]
    try: years=float(profile.get('years_experience',0))
    except (TypeError,ValueError): years=0.0
    req=re.search(r'(\d+)\s*\+?\s*years?',low); reqyears=int(req.group(1)) if req else None
    flags=[]
    if re.search(r'\b(senior|lead|principal|manager|7\+ years|5\+ years)\b',low): flags.append('SENIORITY_SIGNAL: inspect senior/lead responsibilities.')
    if reqyears is not None and reqyears>years: flags.append(f'EXPERIENCE_GAP: vacancy mentions {reqyears}+ years; profile records {years:g}.')
    if re.search(r'\b(registration fee|training fee|pay to apply|upfront fee)\b|\bguaranteed\s+(job|salary|earnings)\b',low): flags.append('PAYMENT_RED_FLAG: independently scrutinise payment or guaranteed-earnings claims.')
    if re.search(r'\b(remote|work from home|wfh)\b',low): flags.append('REMOTE_CLAIM: verify country, state, shift and hybrid restrictions.')
    if re.search(r'\b(passport|aadhaar|bank password|otp|upfront fee)\b',low): flags.append('SENSITIVE_REQUEST_RED_FLAG: do not provide credentials, OTPs or unnecessary identity/banking data.')
    evidence=profile.get('evidence',{})
    em=[{'requirement':s,'candidate_skill_claim':s.lower() in skills,'evidence_status':evidence.get(s,{}).get('status','NOT_PROVIDED'),'evidence_reference':evidence.get(s,{}).get('reference','')} for s in detected]
    qs=[{'topic':s,'question':q} for s in detected for q in QUESTIONS[s]] or [{'topic':'Role analysis','question':'Which outcomes would define success in the first 90 days?'}]
    return {'vacancy_title':title,'generated_on':date.today().isoformat(),'method':'deterministic keyword-based preparation aid; not AI','detected_topics':detected,'matched_profile_skills':matched,'potential_skill_gaps':gaps,'years_experience_in_profile':years,'experience_requirement_signal':reqyears,'risk_flags':flags,'evidence_map':em,'interview_questions':qs,'limitations':['Keyword detection can miss synonyms and context.','A topic match does not prove competence.','No hiring probability, employer verification or vacancy authenticity assessment is produced.','Never disclose identifiable patient information in interviews or portfolio materials.']}
def write_outputs(pack,out):
    out.mkdir(parents=True,exist_ok=True); (out/'interview_pack.json').write_text(json.dumps(pack,indent=2),encoding='utf-8')
    lines=[f"# Interview preparation: {pack['vacancy_title']}",f"Generated: {pack['generated_on']}",f"Method: {pack['method']}",'','## Detected topics',', '.join(pack['detected_topics']) or 'None detected; review manually.','','## Potential skill gaps',', '.join(pack['potential_skill_gaps']) or 'No keyword gaps detected; this does not prove proficiency.','','## Verification flags']
    lines += ['- '+x for x in pack['risk_flags']] or ['- No automated flags; manual verification remains necessary.']
    lines += ['','## Evidence map']+[f"- **{x['requirement']}** — claim: {x['candidate_skill_claim']}; evidence: {x['evidence_status']}; reference: {x['evidence_reference'] or 'not supplied'}" for x in pack['evidence_map']]
    lines += ['','## Practice questions']+[f"{i}. **{x['topic']}** — {x['question']}" for i,x in enumerate(pack['interview_questions'],1)]
    lines += ['','## Limitations']+['- '+x for x in pack['limitations']]
    (out/'interview_pack.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('job_description'); p.add_argument('--profile',required=True); p.add_argument('--title',default='Unspecified role'); p.add_argument('--out',default='output'); a=p.parse_args()
    jd=Path(a.job_description).read_text(encoding='utf-8'); profile=json.loads(Path(a.profile).read_text(encoding='utf-8')); write_outputs(make_pack(jd,profile,a.title),Path(a.out)); print('Interview pack created.')
if __name__=='__main__': main()
