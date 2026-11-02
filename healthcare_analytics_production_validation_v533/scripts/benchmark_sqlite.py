#!/usr/bin/env python3
"""Repeatable SQLite read benchmark for the v5.32 generated warehouse."""
import sqlite3, pathlib, time, json, sys
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[1]
candidates=list((ROOT/"healthcare_analytics_real_world_practicum_v532").rglob("*.sqlite")) + list((ROOT/"healthcare_analytics_real_world_practicum_v532").rglob("*.db"))
if not candidates:
    print("No generated SQLite database found. Run v5.32 src/run_project.py first.")
    sys.exit(2)
db=candidates[0]
con=sqlite3.connect(f"file:{db}?mode=ro",uri=True)
queries=[
 ("table_counts","SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"),
 ("integrity","PRAGMA integrity_check"),
 ("encounter_aggregation","SELECT COUNT(*) FROM fact_encounter"),
]
results=[]
for name,sql in queries:
    t=time.perf_counter()
    try: rows=con.execute(sql).fetchall(); err=None
    except Exception as e: rows=[]; err=str(e)
    results.append({"test":name,"seconds":round(time.perf_counter()-t,6),"rows":len(rows),"error":err})
con.close()
out=HERE.parent/"deliverables"; out.mkdir(exist_ok=True)
(out/"sqlite_benchmark.json").write_text(json.dumps({"database":db.name,"results":results},indent=2))
print(json.dumps(results,indent=2))
