from pathlib import Path
import csv, sqlite3, json, hashlib
BASE=Path(__file__).resolve().parents[1]
DATA=BASE/'data'/'synthetic_hypertension_records.csv'
OUT=BASE/'outputs'
VALID_CLASSES={'ACE inhibitor','ARB','Calcium channel blocker','Thiazide-like diuretic','Beta blocker'}
def num(x):
    try: return float(x) if x not in ('',None) else None
    except (TypeError,ValueError): return None
def run():
    OUT.mkdir(exist_ok=True)
    with DATA.open(newline='') as f: raw=list(csv.DictReader(f))
    seen=set(); clean=[]; issues=[]
    for row in raw:
        rid=row['record_id']
        if rid in seen:
            issues.append({'record_id':rid,'issue':'duplicate_record_id'}); continue
        seen.add(rid)
        if row['primary_drug_class'] not in VALID_CLASSES:
            issues.append({'record_id':rid,'issue':'missing_or_unknown_primary_drug_class'}); continue
        b=num(row['baseline_sbp_mmhg']); fu=num(row['followup_sbp_mmhg'])
        if fu is None: issues.append({'record_id':rid,'issue':'missing_followup_sbp'})
        if num(row['followup_dbp_mmhg']) is None: issues.append({'record_id':rid,'issue':'missing_followup_dbp'})
        if b is None or not 70<=b<=250:
            issues.append({'record_id':rid,'issue':'invalid_baseline_sbp'}); continue
        if fu is not None and not 70<=fu<=250:
            issues.append({'record_id':rid,'issue':'implausible_followup_sbp'}); fu=None
        row['_baseline_sbp']=b; row['_followup_sbp']=fu
        clean.append(row)
    paired=[r for r in clean if r['_followup_sbp'] is not None]
    groups={}
    for r in paired:
        groups.setdefault(r['primary_drug_class'],[]).append(r)
    summary=[]
    for cls,rs in sorted(groups.items()):
        changes=[r['_baseline_sbp']-r['_followup_sbp'] for r in rs]
        summary.append({'primary_drug_class':cls,'paired_n':len(rs),'mean_baseline_sbp':round(sum(r['_baseline_sbp'] for r in rs)/len(rs),2),'mean_followup_sbp':round(sum(r['_followup_sbp'] for r in rs)/len(rs),2),'mean_change_sbp':round(sum(changes)/len(changes),2)})
    # This is an explicitly illustrative operational threshold, not an individualized treatment goal.
    controlled=sum(1 for r in paired if r['_followup_sbp']<140 and num(r['followup_dbp_mmhg']) is not None and num(r['followup_dbp_mmhg'])<90)
    metrics={'raw_rows':len(raw),'unique_record_ids':len(seen),'clean_rows':len(clean),'paired_sbp_rows':len(paired),'excluded_rows':len(raw)-len(clean),'quality_issue_count':len(issues),'illustrative_followup_bp_below_140_90_n':controlled,'illustrative_followup_bp_below_140_90_pct':round(100*controlled/len(paired),2) if paired else None,'interpretation_note':'The <140/90 mmHg flag is an educational analytic convention only. Individual targets vary; this dataset cannot guide patient care.'}
    (OUT/'quality_and_summary.json').write_text(json.dumps({'metrics':metrics,'by_primary_drug_class':summary,'quality_issues':issues},indent=2))
    with (OUT/'drug_class_summary.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(summary[0]) if summary else ['primary_drug_class','paired_n','mean_baseline_sbp','mean_followup_sbp','mean_change_sbp']);w.writeheader();w.writerows(summary)
    db=OUT/'hypertension_analysis.sqlite'
    if db.exists(): db.unlink()
    con=sqlite3.connect(db)
    con.executescript((BASE/'sql'/'schema.sql').read_text())
    cols=['record_id','age_years','sex','diabetes','ckd','ischemic_heart_disease','primary_drug_class','regimen_classes','antihypertensive_count','adherence_category','baseline_sbp_mmhg','baseline_dbp_mmhg','followup_sbp_mmhg','followup_dbp_mmhg','followup_days']
    con.executemany('INSERT INTO hypertension_records VALUES ('+','.join('?' for _ in cols)+')',[[r[c] or None for c in cols] for r in clean])
    con.commit();con.close()
    return metrics
if __name__=='__main__': print(json.dumps(run(),indent=2))
