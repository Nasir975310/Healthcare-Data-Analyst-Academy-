#!/usr/bin/env python3
"""Explainable job-description fit assessment. Standard library only; advisory, not predictive."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

SKILL_GROUPS = {
    "sql": ["sql", "postgresql", "mysql", "sqlite", "sql server"],
    "python": ["python", "pandas", "numpy"],
    "excel": ["excel", "pivot table", "power query"],
    "bi": ["power bi", "tableau", "looker", "dashboard", "dax"],
    "statistics": ["statistics", "statistical analysis", "hypothesis testing", "regression"],
    "healthcare": ["healthcare", "clinical", "hospital", "pharmacy", "pharmd", "pharm.d", "medical records"],
    "research": ["clinical research", "gcp", "pharmacovigilance", "drug safety", "real-world evidence", "rwe"],
    "data_quality": ["data quality", "data validation", "data cleaning", "data governance"],
    "communication": ["stakeholder", "communication", "presentation", "report writing"],
}
ROLE_TERMS = {
    "Healthcare Data Analyst": ["healthcare data analyst", "health data analyst", "healthcare analytics"],
    "Clinical Data Analyst / Coordinator": ["clinical data analyst", "clinical data coordinator", "clinical data management"],
    "Clinical Research Data Coordinator": ["clinical research coordinator", "research data coordinator", "clinical trial data"],
    "Pharmacovigilance / Drug Safety": ["pharmacovigilance", "drug safety", "safety associate", "case processing"],
    "Healthcare Reporting / MIS": ["mis analyst", "reporting analyst", "healthcare reporting", "business intelligence analyst"],
    "Real-World Evidence Analyst": ["real-world evidence", "rwe analyst", "observational research"],
}
RED_FLAGS = {
    "upfront_fee": [r"registration fee", r"training fee", r"pay.*deposit", r"security deposit", r"application fee"],
    "sensitive_data_request": [r"share.*otp", r"bank password", r"card cvv", r"send.*aadhaar", r"passport.*whatsapp"],
    "unrealistic_pay_claim": [r"guaranteed.*income", r"earn.*per day", r"no experience.*\b[5-9]\d{4,}\b", r"100% placement guarantee"],
    "vague_employer_or_contact": [r"whatsapp only", r"telegram only", r"no interview.*instant", r"company details.*later"],
}

DEFAULT_PROFILE = {
    "education": "Pharm.D final year / completing; verify exact status before use",
    "skills": ["Excel", "SQL", "Python", "pandas", "NumPy", "Matplotlib", "statistics", "healthcare domain", "clinical research", "data quality"],
    "experience_years": 0,
    "location": "India",
    "remote_preference": True,
    "evidence": ["Pharm.D thesis: prospective observational antihypertensive drug-utilization evaluation, N=153", "Separate synthetic healthcare analytics portfolio projects"],
}

def _contains(text, terms):
    t=text.lower()
    return [term for term in terms if term.lower() in t]

def assess(jd: str, profile: dict | None=None) -> dict:
    if not jd or not jd.strip(): raise ValueError('Job description is empty.')
    p=profile or DEFAULT_PROFILE
    text=jd.lower()
    found={k:_contains(jd,v) for k,v in SKILL_GROUPS.items()}
    profile_skills=[str(x).lower() for x in p.get('skills',[])]
    matched=[]; missing=[]
    for group, terms in found.items():
        if terms:
            if any(any(skill==t.lower() or t.lower() in skill or skill in t.lower() for skill in profile_skills) for t in terms): matched.append(group)
            else: missing.append(group)
    # Weighted dimensions, each independently explainable.
    skill_score=round(35*len(matched)/max(1,len([x for x in found.values() if x]))) if any(found.values()) else 0
    education_terms=[x for x in ['pharmd','pharm.d','pharmacy','life sciences','life science','biomedical','healthcare'] if x in text]
    education_score=15 if education_terms and any(x in p.get('education','').lower() for x in ['pharmd','pharm.d','pharmacy','life science','healthcare']) else (10 if not re.search(r"master's required|phd required|mbbs required|\bdoctorate required\b",text) else 0)
    ranges=re.findall(r'\b(\d+)\s*(?:-|to)\s*(\d+)\s+years?\s+(?:of\s+)?(?:experience|exp)',text)
    years=re.findall(r'(?:minimum|min\.?|at least|required|\b)(?<![-\d])(\d+)\+?\s+years?\s+(?:of\s+)?(?:experience|exp)',text)
    required_years=max([int(a) for a,b in ranges]+list(map(int,years)),default=0)
    exp_years=float(p.get('experience_years',0) or 0)
    experience_score=15 if required_years<=exp_years else max(0,round(15*(exp_years/required_years))) if required_years else 15
    remote_terms=any(x in text for x in ['remote','work from home','wfh','hybrid'])
    remote_score=10 if (not p.get('remote_preference') or remote_terms) else 5
    domain_score=10 if any(x in text for x in ['healthcare','hospital','clinical','pharma','pharmacy','medical','drug safety']) else 4
    must=re.findall(r'(?:must have|required|mandatory|essential)[:\s-]+([^.;\n]+)',jd,re.I)
    must_text=' '.join(must).lower()
    must_missing=[s for s in profile_skills if False]
    # Identify explicit seniority and credential barriers without treating keywords as proof.
    senior=bool(re.search(r'\bsenior\b|\blead\b|\bmanager\b|\bprincipal\b|\bhead of\b',text))
    degree_barrier=bool(re.search(r"master's degree required|phd required|mbbs required|\bmd required\b",text))
    red={k:[pat for pat in pats if re.search(pat,text,re.I)] for k,pats in RED_FLAGS.items()}
    red={k:v for k,v in red.items() if v}
    score=min(100,skill_score+education_score+experience_score+remote_score+domain_score+15)
    if senior: score=max(0,score-15)
    if degree_barrier: score=max(0,score-20)
    if red: score=max(0,score- min(25,10*len(red)))
    if score>=75 and not red and not degree_barrier: recommendation='PRIORITISE'
    elif score>=55 and not red: recommendation='REVIEW_REQUIREMENTS'
    else: recommendation='LOW_PRIORITY_OR_AVOID'
    roles=[name for name,terms in ROLE_TERMS.items() if _contains(jd,terms)]
    return {
      'assessment_type':'deterministic_advisory_job_fit','score_out_of_100':score,'recommendation':recommendation,
      'not_a_hiring_probability':True,'role_families_detected':roles,
      'dimension_scores':{'skills_and_tools_out_of_35':skill_score,'education_out_of_15':education_score,'experience_out_of_15':experience_score,'remote_alignment_out_of_10':remote_score,'healthcare_domain_out_of_10':domain_score,'baseline_transferable_fit_out_of_15':15},
      'matched_skill_groups':matched,'skill_groups_not_evidenced_in_profile':missing,'job_skills_detected':found,
      'required_experience_years_detected':required_years,'profile_experience_years':exp_years,
      'senior_role_language_detected':senior,'higher_degree_barrier_detected':degree_barrier,
      'risk_flags':red,'interpretation':'A keyword match is not proof of competence. Verify every requirement and employer independently; tailor only claims supported by evidence.'
    }

def render_report(r):
    lines=['# Job Fit Assessment', '', f"**Advisory score:** {r['score_out_of_100']}/100", f"**Recommendation:** {r['recommendation']}", '', '> This deterministic heuristic is not an ATS score and does not estimate the probability of being hired.', '', '## Score breakdown']
    for k,v in r['dimension_scores'].items(): lines.append(f'- {k.replace("_"," ")}: {v}')
    lines += ['', '## Role families detected'] + ([f'- {x}' for x in r['role_families_detected']] or ['- No clear family detected'])
    lines += ['', '## Skill evidence']
    lines += ['- Matched groups: '+(', '.join(r['matched_skill_groups']) or 'None detected')]
    lines += ['- Gaps to review: '+(', '.join(r['skill_groups_not_evidenced_in_profile']) or 'None detected')]
    lines += ['', '## Risk and fit checks', f"- Experience requested: {r['required_experience_years_detected']} years; profile: {r['profile_experience_years']} years", f"- Senior wording: {'Yes' if r['senior_role_language_detected'] else 'No'}", f"- Higher-degree barrier: {'Yes' if r['higher_degree_barrier_detected'] else 'No'}"]
    for k,v in r['risk_flags'].items(): lines.append(f'- **Risk flag — {k}:** {", ".join(v)}')
    if not r['risk_flags']: lines.append('- No listed textual red flags detected; this does not verify the employer.')
    lines += ['', '## Required human review', '- Confirm employer identity, official domain, job location, salary and employment type.', '- Separate mandatory from preferred criteria; inspect the full description.', '- Do not claim a skill unless you can demonstrate it.', '- Never pay recruitment, registration or training fees to obtain a job; do not share OTPs, passwords or card credentials.', '', r['interpretation']]
    return '\n'.join(lines)+'\n'

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('job_description',help='Path to a UTF-8 text file containing the job description')
    ap.add_argument('--profile',help='Optional JSON profile file; defaults to the documented Pharm.D entry-level profile')
    ap.add_argument('--out',default='jobfit_output',help='Output directory (default: jobfit_output)')
    a=ap.parse_args(); jd=Path(a.job_description).read_text(encoding='utf-8')
    p=json.loads(Path(a.profile).read_text(encoding='utf-8')) if a.profile else None
    result=assess(jd,p); out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
    (out/'assessment.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    (out/'assessment.md').write_text(render_report(result),encoding='utf-8')
    print(render_report(result))
if __name__=='__main__': main()
