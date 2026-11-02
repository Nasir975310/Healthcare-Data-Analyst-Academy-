#!/usr/bin/env python3
"""Profile-limited synthetic FHIR R4 ingestion and healthcare analytics ETL demo."""
import argparse, csv, hashlib, json, re, sqlite3
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

SUPPORTED={"Patient","Encounter","Observation","MedicationRequest"}
DATE_RE=re.compile(r"^\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:\d{2})?)?$")
def readj(p):
    with open(p,encoding="utf-8") as f: return json.load(f)
def valid_date(v):
    if not isinstance(v,str) or not DATE_RE.match(v): return False
    try: datetime.fromisoformat(v.replace("Z","+00:00")); return True
    except ValueError: return False
def validate_bundle(b):
    errors=[]; warnings=[]; resources=[]; ids=set()
    if b.get("resourceType")!="Bundle": errors.append("Root resourceType must be Bundle")
    entries=b.get("entry",[])
    if not isinstance(entries,list): errors.append("Bundle.entry must be an array"); entries=[]
    for i,e in enumerate(entries):
        r=e.get("resource") if isinstance(e,dict) else None
        if not isinstance(r,dict): errors.append(f"entry[{i}] missing resource object"); continue
        typ,rid=r.get("resourceType"),r.get("id")
        if typ not in SUPPORTED: errors.append(f"entry[{i}] unsupported resourceType {typ}"); continue
        if not isinstance(rid,str) or not rid: errors.append(f"entry[{i}] {typ} requires id")
        elif (typ,rid) in ids: errors.append(f"duplicate resource id {typ}/{rid}")
        else: ids.add((typ,rid))
        resources.append(r)
        if typ=="Encounter":
            p=r.get("period",{})
            if not valid_date(p.get("start")): errors.append(f"Encounter/{rid}: invalid period.start")
            if p.get("end") and not valid_date(p["end"]): errors.append(f"Encounter/{rid}: invalid period.end")
        if typ=="Observation":
            if not valid_date(r.get("effectiveDateTime")): errors.append(f"Observation/{rid}: invalid effectiveDateTime")
            if not r.get("subject",{}).get("reference"): errors.append(f"Observation/{rid}: missing subject.reference")
            if not r.get("code",{}).get("coding"): warnings.append(f"Observation/{rid}: no coding")
        if typ=="MedicationRequest" and not r.get("subject",{}).get("reference"):
            errors.append(f"MedicationRequest/{rid}: missing subject.reference")
    known={f'{r.get("resourceType")}/{r.get("id")}' for r in resources}
    for r in resources:
        for key in ("subject","patient","encounter"):
            ref=r.get(key,{}).get("reference") if isinstance(r.get(key),dict) else None
            if ref and ref.startswith(("Patient/","Encounter/")) and ref not in known:
                errors.append(f'{r.get("resourceType")}/{r.get("id")}: unresolved {key} reference {ref}')
    return {"valid":not errors,"errors":errors,"warnings":warnings,"checked_resources":len(resources),
            "resource_counts":dict(Counter(r["resourceType"] for r in resources)),
            "validation_scope":"Limited local structural checks; not full FHIR R4 conformance."}
def flatten(b,cfg):
    out={"patients":[],"encounters":[],"observations":[],"medications":[]}
    mappings=cfg.get("terminology",{}).get("mappings",{})
    for e in b.get("entry",[]):
        r=e.get("resource",{}); typ=r.get("resourceType"); rid=r.get("id")
        if typ=="Patient":
            n=(r.get("name") or [{}])[0]
            out["patients"].append({"patient_id":rid,"gender":r.get("gender"),"birth_date":r.get("birthDate"),
                "display_name_synthetic":" ".join(n.get("given",[])+[n.get("family","")]).strip()})
        elif typ=="Encounter":
            out["encounters"].append({"encounter_id":rid,"patient_id":r.get("subject",{}).get("reference","").replace("Patient/",""),
                "status":r.get("status"),"class_code":r.get("class",{}).get("code"),
                "start":r.get("period",{}).get("start"),"end":r.get("period",{}).get("end")})
        elif typ=="Observation":
            c=(r.get("code",{}).get("coding") or [{}])[0]; q=r.get("valueQuantity",{})
            m=mappings.get(f'{c.get("system","")}|{c.get("code","")}',{})
            out["observations"].append({"observation_id":rid,"patient_id":r.get("subject",{}).get("reference","").replace("Patient/",""),
                "encounter_id":r.get("encounter",{}).get("reference","").replace("Encounter/",""),
                "effective_datetime":r.get("effectiveDateTime"),"source_system":c.get("system"),"source_code":c.get("code"),
                "display":c.get("display"),"mapped_concept":m.get("target_display"),"mapped_system":m.get("target_system"),
                "value":q.get("value"),"unit":q.get("unit"),"unit_code":q.get("code")})
        elif typ=="MedicationRequest":
            c=(r.get("medicationCodeableConcept",{}).get("coding") or [{}])[0]
            out["medications"].append({"medication_request_id":rid,"patient_id":r.get("subject",{}).get("reference","").replace("Patient/",""),
                "encounter_id":r.get("encounter",{}).get("reference","").replace("Encounter/",""),
                "authored_on":r.get("authoredOn"),"status":r.get("status"),"source_system":c.get("system"),
                "source_code":c.get("code"),"medication_display":c.get("display")})
    return out
def quality(t):
    pids={x["patient_id"] for x in t["patients"]}; eids={x["encounter_id"] for x in t["encounters"]}
    checks=[
      ("duplicate_patient_id",len(t["patients"])-len(pids),"error",""),
      ("orphan_encounter_patient",sum(x["patient_id"] not in pids for x in t["encounters"]),"error",""),
      ("orphan_observation_patient",sum(x["patient_id"] not in pids for x in t["observations"]),"error",""),
      ("orphan_observation_encounter",sum(bool(x["encounter_id"]) and x["encounter_id"] not in eids for x in t["observations"]),"error",""),
      ("orphan_medication_patient",sum(x["patient_id"] not in pids for x in t["medications"]),"error",""),
      ("unmapped_observation_code",sum(not x["mapped_concept"] for x in t["observations"]),"warning","Illustrative mappings only; not authoritative crosswalks."),
      ("observation_missing_value",sum(x["value"] is None for x in t["observations"]),"warning","")]
    return {"checks":[{"rule":a,"issue_count":b,"severity":c,"detail":d} for a,b,c,d in checks],
      "total_issues":sum(x[1] for x in checks),"interpretation":"Flags require review; they do not establish clinical validity."}
def longitudinal(t):
    ob=defaultdict(list); me=defaultdict(list); patients={x["patient_id"]:x for x in t["patients"]}
    for x in t["observations"]: ob[(x["patient_id"],x["encounter_id"])].append(x)
    for x in t["medications"]: me[(x["patient_id"],x["encounter_id"])].append(x)
    rows=[]
    for e in t["encounters"]:
        k=(e["patient_id"],e["encounter_id"]); oo=ob[k]; mm=me[k]; p=patients.get(e["patient_id"],{})
        nums=[x["value"] for x in oo if isinstance(x["value"],(int,float))]
        rows.append({"patient_id":e["patient_id"],"encounter_id":e["encounter_id"],"gender":p.get("gender"),
          "birth_date":p.get("birth_date"),"encounter_status":e["status"],"encounter_start":e["start"],
          "encounter_end":e["end"],"observation_count":len(oo),"medication_request_count":len(mm),
          "numeric_observation_mean":sum(nums)/len(nums) if nums else None,
          "observation_concepts":"; ".join(sorted({x["mapped_concept"] or x["display"] or "unmapped" for x in oo})),
          "medications":"; ".join(sorted({x["medication_display"] or "unknown" for x in mm}))})
    return rows
def build_cohort(t,cfg):
    statuses=cfg.get("cohort",{}).get("required_encounter_status",["finished"])
    eligible=[e for e in t["encounters"] if e["status"] in statuses]
    ids=sorted({e["patient_id"] for e in eligible})
    return {"cohort_name":cfg.get("cohort",{}).get("name","Synthetic cohort"),
      "criteria":{"encounter_status_in":statuses},"screened_encounters":len(t["encounters"]),
      "eligible_encounters":len(eligible),"unique_patients":len(ids),"patient_ids":ids,
      "flow":[{"stage":"All encounters","n":len(t["encounters"])},{"stage":"Eligible encounters","n":len(eligible)},
              {"stage":"Unique patients","n":len(ids)}],
      "index_date_definition":"Encounter start date; not a causal treatment index date."}
def write_csv(p,rows):
    if not rows: p.write_text("",encoding="utf-8"); return
    with p.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
def main():
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument("--input",required=True); ap.add_argument("--config",required=True); ap.add_argument("--output",required=True)
    a=ap.parse_args(); out=Path(a.output); out.mkdir(parents=True,exist_ok=True)
    b=readj(a.input); cfg=readj(a.config); v=validate_bundle(b)
    (out/"validation_report.json").write_text(json.dumps(v,indent=2),encoding="utf-8")
    if not v["valid"]: raise SystemExit("Validation failed; inspect validation_report.json")
    t=flatten(b,cfg); q=quality(t); lr=longitudinal(t); co=build_cohort(t,cfg)
    for n,rows in t.items(): write_csv(out/f"{n}.csv",rows)
    write_csv(out/"patient_encounter_longitudinal.csv",lr)
    for n,obj in [("data_quality_report.json",q),("cohort_definition_and_flow.json",co),
                  ("data_dictionary.json",cfg.get("data_dictionary",{}))]:
        (out/n).write_text(json.dumps(obj,indent=2),encoding="utf-8")
    with sqlite3.connect(out/"hospital_analytics.sqlite") as db:
        for n,rows in {**t,"patient_encounter_longitudinal":lr}.items():
            if not rows: continue
            cols=list(rows[0]); quoted=",".join('"'+c+'"' for c in cols)
            db.execute(f'CREATE TABLE "{n}" ({quoted})')
            db.executemany(f'INSERT INTO "{n}" VALUES ({",".join("?" for _ in cols)})',
                [[json.dumps(v) if isinstance(v,(dict,list)) else v for v in r.values()] for r in rows])
    manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.iterdir()) if p.is_file() and p.name!="sha256_manifest.json"}
    (out/"sha256_manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
    print(json.dumps({"status":"success","validation":v,"quality_total_issues":q["total_issues"],
      "table_rows":{k:len(vv) for k,vv in t.items()},"longitudinal_rows":len(lr),
      "cohort_unique_patients":co["unique_patients"],"output":str(out)},indent=2))
if __name__=="__main__": main()
