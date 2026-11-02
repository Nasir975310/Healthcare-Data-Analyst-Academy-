#!/usr/bin/env python3
"""Machine-checkable core of the v5.35 assessment. Manual rubric remains required."""
import pathlib, sqlite3, json, sys
HERE=pathlib.Path(__file__).resolve().parent
ACADEMY=HERE.parents[1]
DB=ACADEMY/"healthcare_analytics_real_world_practicum_v532/deliverables/hospital_analytics.sqlite"
checks=[]
def add(name, ok, detail, points):
    checks.append({"item":name,"pass":bool(ok),"points_awarded":points if ok else 0,
                   "points_possible":points,"detail":detail})
def main():
    if not DB.exists():
        print("Run v5.32 pipeline first; SQLite warehouse not found.",file=sys.stderr)
        return 2
    con=sqlite3.connect(f"file:{DB}?mode=ro",uri=True)
    tables={r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    required={"dim_patient","stg_encounter","fact_encounter","fact_observation","fact_medication"}
    add("warehouse_tables",required.issubset(tables),f"tables={sorted(tables)}",5)
    if required.issubset(tables):
        raw=con.execute("SELECT COUNT(*) FROM stg_encounter").fetchone()[0]
        accepted=con.execute("SELECT COUNT(*) FROM fact_encounter").fetchone()[0]
        orphan=con.execute("""SELECT COUNT(*) FROM stg_encounter s LEFT JOIN dim_patient p
            ON p.patient_id=s.patient_id WHERE p.patient_id IS NULL""").fetchone()[0]
        add("raw_accepted_rejected",raw==91 and accepted==90 and raw-accepted==1,
            f"raw={raw}, accepted={accepted}, rejected={raw-accepted}",10)
        add("orphan_detection",orphan==1,f"orphan_rows={orphan}",10)
        integrity=con.execute("PRAGMA integrity_check").fetchone()[0]
        fk=con.execute("PRAGMA foreign_key_check").fetchall()
        add("warehouse_integrity",integrity=="ok" and not fk,
            f"integrity={integrity}; fk_violations={len(fk)}",5)
        enc,patients=con.execute("SELECT COUNT(*),COUNT(DISTINCT patient_id) FROM fact_encounter").fetchone()
        add("encounter_patient_distinction",enc==90 and patients<=enc,
            f"encounters={enc}, unique_patients={patients}",5)
        meds=con.execute("SELECT COUNT(*) FROM fact_medication").fetchone()[0]
        add("medication_order_scope",meds==129,f"medication_order_rows={meds}",5)
    con.close()
    result={"assessment":"v5.35 machine-checkable core",
            "automated_points":sum(x["points_awarded"] for x in checks),
            "automated_possible":sum(x["points_possible"] for x in checks),
            "checks":checks,"manual_review_required":True,
            "full_rubric":"assessments/SCORING_RUBRIC.md"}
    out=HERE.parent/"assessment_results.json"
    out.write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
    return 0 if all(x["pass"] for x in checks) else 1
if __name__=="__main__":
    sys.exit(main())
