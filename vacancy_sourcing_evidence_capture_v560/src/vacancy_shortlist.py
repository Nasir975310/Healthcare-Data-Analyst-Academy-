"""Capture, deduplicate and prioritise manually sourced vacancies without inventing live listings."""
from __future__ import annotations
import argparse, csv, json, re, hashlib, html
from pathlib import Path
from datetime import date, datetime, timezone
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

FIELDS = [
    "vacancy_id","employer","role","source_name","source_type","source_url",
    "employer_official_url","captured_at","date_found","deadline","location",
    "remote_type","employment_type","required_experience_years","education_requirement",
    "required_skills","preferred_skills","job_description_excerpt","eligibility_notes",
    "evidence_file","evidence_sha256","status"
]
STAGES = {"new","shortlisted","not_suitable","verification_pending","verified_by_user","applied","expired","closed"}
TRACKING = {"utm_source","utm_medium","utm_campaign","utm_term","utm_content","gclid","fbclid"}
SKILL_ALIASES = {
    "SQL": ["sql","postgresql","mysql","sqlite"],
    "Python": ["python","pandas","numpy"],
    "Excel": ["excel","pivot table","power query"],
    "Power BI": ["power bi","powerbi","dax"],
    "Statistics": ["statistics","hypothesis testing","regression","confidence interval"],
    "R": ["r programming","rstudio","r language"],
    "Healthcare": ["healthcare","clinical","hospital","patient","pharmacy","pharmacovigilance"],
    "Research": ["clinical research","observational study","research","study design"],
    "Data quality": ["data quality","validation","data cleaning","missing data","deduplication"],
    "Communication": ["stakeholder","communication","presentation","reporting"]
}

def canonical_url(url):
    raw=(url or "").strip()
    if not raw: return ""
    p=urlsplit(raw)
    scheme=(p.scheme or "https").lower()
    host=(p.hostname or "").lower()
    if not host: return raw.lower().rstrip("/")
    port=p.port
    netloc=host
    if port and not ((scheme=="https" and port==443) or (scheme=="http" and port==80)):
        netloc += f":{port}"
    path=re.sub(r"/+","/",p.path or "/").rstrip("/") or "/"
    query=sorted((k,v) for k,v in parse_qsl(p.query,keep_blank_values=True) if k.lower() not in TRACKING)
    return urlunsplit((scheme,netloc,path,urlencode(query),""))

def norm_text(value):
    return re.sub(r"\s+"," ",(value or "").strip().lower())

def parse_list(value):
    return [x.strip() for x in re.split(r"[;,|]",value or "") if x.strip()]

def load_rows(path):
    with open(path,newline="",encoding="utf-8-sig") as f:
        reader=csv.DictReader(f)
        missing=[x for x in FIELDS if x not in (reader.fieldnames or [])]
        if missing: raise ValueError("Missing columns: "+", ".join(missing))
        rows=list(reader)
    seen=set()
    for i,r in enumerate(rows,2):
        vid=(r.get("vacancy_id") or "").strip()
        if not vid: raise ValueError(f"Row {i}: vacancy_id required.")
        if vid in seen: raise ValueError(f"Row {i}: duplicate vacancy_id {vid!r}.")
        seen.add(vid)
        stage=(r.get("status") or "").strip().lower()
        if stage not in STAGES: raise ValueError(f"Row {i}: invalid status {stage!r}.")
        for fld in ("date_found","deadline"):
            v=(r.get(fld) or "").strip()
            if v:
                try: date.fromisoformat(v)
                except ValueError as e: raise ValueError(f"Row {i}: {fld} must be YYYY-MM-DD.") from e
        url=(r.get("source_url") or "").strip()
        if url and urlsplit(url).scheme not in {"http","https"}: raise ValueError(f"Row {i}: unsafe source_url.")
        exp=(r.get("required_experience_years") or "").strip()
        if exp:
            try:
                if float(exp)<0: raise ValueError()
            except ValueError as e: raise ValueError(f"Row {i}: required_experience_years must be non-negative numeric.") from e
    return rows

def duplicate_groups(rows):
    buckets={}
    for r in rows:
        u=canonical_url(r.get("source_url"))
        if u: buckets.setdefault(("url",u),[]).append(r["vacancy_id"])
        # Secondary heuristic: same employer + role + location; review manually.
        key=("text",norm_text(r.get("employer")),norm_text(r.get("role")),norm_text(r.get("location")))
        if all(key[1:]): buckets.setdefault(key,[]).append(r["vacancy_id"])
    groups = {tuple(sorted(set(ids))) for ids in buckets.values() if len(set(ids))>1}
    return [list(group) for group in sorted(groups)]

def profile_match(row, profile):
    jd=norm_text(" ".join([row.get("role",""),row.get("job_description_excerpt",""),row.get("required_skills",""),row.get("preferred_skills","")]))
    detected=[]
    for skill,terms in SKILL_ALIASES.items():
        if any(norm_text(t) in jd for t in terms): detected.append(skill)
    candidate={norm_text(x):x for x in profile.get("skills",[])}
    matched=[s for s in detected if norm_text(s) in candidate]
    gaps=[s for s in detected if norm_text(s) not in candidate]
    must=parse_list(row.get("required_skills"))
    must_matched=[s for s in must if any(norm_text(s)==norm_text(x) for x in profile.get("skills",[]))]
    must_gaps=[s for s in must if s not in must_matched]
    exp_req=float(row.get("required_experience_years") or 0)
    exp_user=float(profile.get("years_experience",0) or 0)
    exp_gap=exp_req>exp_user
    # Transparent prioritisation score, not hiring probability.
    score=0
    score += min(30, round(30*len(matched)/max(1,len(detected))))
    score += 30 if norm_text("healthcare") in {norm_text(x) for x in profile.get("domains",[])} and "Healthcare" in detected else 0
    score += 20 if not exp_gap else 0
    score += 20 if not must_gaps else max(0,20-5*len(must_gaps))
    return {
        "detected_skill_topics":detected,"profile_skill_matches":matched,"potential_skill_gaps":gaps,
        "required_skills":must,"required_skills_not_in_profile":must_gaps,
        "experience_requirement_years":exp_req,"profile_years_experience":exp_user,
        "experience_gap_signal":exp_gap,"priority_score":min(100,score),
        "priority_label":"Review" if score>=70 else ("Consider" if score>=40 else "Low priority"),
        "score_caution":"Heuristic prioritisation aid only; not an ATS score, qualification judgement or hiring probability."
    }

def build_report(rows, profile, as_of):
    items=[]
    for r in rows:
        deadline=(r.get("deadline") or "").strip()
        expired=bool(deadline and date.fromisoformat(deadline)<as_of)
        match=profile_match(r,profile)
        items.append({
            "vacancy_id":r["vacancy_id"],"employer":r.get("employer",""),"role":r.get("role",""),
            "source_url":r.get("source_url",""),"captured_at":r.get("captured_at",""),
            "deadline":deadline,"expired":expired,"status":r.get("status",""),
            "source_evidence_sha256":r.get("evidence_sha256",""),"match":match
        })
    items.sort(key=lambda x:(x["expired"],-x["match"]["priority_score"],x["deadline"] or "9999-12-31"))
    return {
        "review_date":as_of.isoformat(),"vacancy_count":len(rows),
        "duplicate_groups":duplicate_groups(rows),
        "active_count":sum(not x["expired"] for x in items),
        "shortlist_count":sum(x["status"]=="shortlisted" and not x["expired"] for x in items),
        "items":items,
        "limitations":[
            "Vacancies must be collected by the user from external sources; this tool does not browse or fetch live listings.",
            "Source evidence is only as reliable as the excerpt/file supplied and does not establish that the vacancy remains open.",
            "Duplicate groups are heuristic; different URLs or changed job titles can evade detection.",
            "Priority scores are transparent heuristics, not hiring probabilities or verified qualification assessments.",
            "Keep personal application information and confidential communications out of public repositories."
        ]
    }

def html_report(report):
    trs=[]
    for x in report["items"]:
        m=x["match"]; status="Expired" if x["expired"] else html.escape(x["status"])
        url=x["source_url"]
        link=f'<a rel="noopener noreferrer" href="{html.escape(url,quote=True)}">Source</a>' if url else "No URL"
        trs.append(f"<tr><td>{html.escape(x['vacancy_id'])}</td><td>{html.escape(x['employer'])}</td><td>{html.escape(x['role'])}</td><td>{status}</td><td>{m['priority_score']}/100 · {m['priority_label']}</td><td>{html.escape(', '.join(m['required_skills_not_in_profile']) or '—')}</td><td>{link}</td></tr>")
    dups="".join("<li>"+html.escape(", ".join(g))+"</li>" for g in report["duplicate_groups"]) or "<li>None detected</li>"
    lim="".join("<li>"+html.escape(x)+"</li>" for x in report["limitations"])
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Vacancy shortlist</title><style>body{{font:15px system-ui;max-width:1200px;margin:2rem auto;padding:0 1rem;color:#202938;background:#f7f8fa}}section{{background:white;border:1px solid #dce1e8;border-radius:12px;padding:16px;margin:14px 0;overflow:auto}}table{{border-collapse:collapse;width:100%;min-width:800px}}td,th{{padding:9px;text-align:left;border-bottom:1px solid #e5e8ed;vertical-align:top}}.muted{{color:#586579}}</style></head><body><h1>Vacancy sourcing & shortlist</h1><p class="muted">Review date {report['review_date']} · {report['vacancy_count']} records · {report['active_count']} not expired by recorded deadline</p><section><h2>Duplicate candidates</h2><ul>{dups}</ul></section><section><h2>Prioritised vacancy list</h2><table><tr><th>ID</th><th>Employer</th><th>Role</th><th>Status</th><th>Priority</th><th>Required skill gaps</th><th>Source</th></tr>{''.join(trs)}</table></section><section><h2>Limitations</h2><ul>{lim}</ul></section></body></html>"""

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("registry");p.add_argument("--profile",required=True);p.add_argument("--as-of",required=True);p.add_argument("--out",default="shortlist_output")
    a=p.parse_args()
    rows=load_rows(a.registry)
    profile=json.loads(Path(a.profile).read_text(encoding="utf-8"))
    report=build_report(rows,profile,date.fromisoformat(a.as_of))
    out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    (out/"shortlist.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    (out/"shortlist.html").write_text(html_report(report),encoding="utf-8")
    print(f"Processed {len(rows)} vacancies; outputs: {out/'shortlist.json'}, {out/'shortlist.html'}")

if __name__=="__main__":main()
