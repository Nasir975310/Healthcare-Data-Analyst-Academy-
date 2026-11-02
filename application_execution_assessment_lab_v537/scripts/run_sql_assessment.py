from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import argparse, json, sqlite3, csv

QUERIES = {
 "source_and_distinct_ids": "SELECT COUNT(*) AS source_rows, COUNT(DISTINCT encounter_id) AS distinct_encounter_ids FROM encounters",
 "status_counts": "SELECT status, COUNT(*) AS row_count FROM encounters GROUP BY status ORDER BY status",
 "department_wait": "SELECT department, COUNT(*) AS completed_rows, ROUND(AVG(wait_minutes),2) AS mean_wait_minutes FROM encounters WHERE status='completed' AND wait_minutes >= 0 AND wait_minutes IS NOT NULL AND department IS NOT NULL GROUP BY department ORDER BY department",
 "duplicate_ids": "SELECT encounter_id, COUNT(*) AS row_count FROM encounters GROUP BY encounter_id HAVING COUNT(*) > 1",
 "weekly_volume": "SELECT strftime('%Y-%W', encounter_date) AS calendar_week, COUNT(*) AS completed_encounters FROM encounters WHERE status='completed' AND encounter_date IS NOT NULL GROUP BY calendar_week ORDER BY calendar_week",
 "invalid_records": "SELECT encounter_id, department, encounter_date, wait_minutes FROM encounters WHERE department IS NULL OR encounter_date IS NULL OR wait_minutes < 0"
}

def run(db, output):
    db=Path(db)
    needs_fixture=not db.exists()
    if not needs_fixture:
        try:
            with sqlite3.connect(db) as check:
                needs_fixture=check.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='encounters'").fetchone() is None
        except sqlite3.DatabaseError:
            needs_fixture=True
    if needs_fixture:
        from create_fixture import build
        build(db)
    output=Path(output); output.mkdir(parents=True,exist_ok=True)
    result={}
    with sqlite3.connect(db) as con:
        con.row_factory=sqlite3.Row
        for key,sql in QUERIES.items():
            result[key]=[dict(r) for r in con.execute(sql).fetchall()]
    (output/'assessment_results.json').write_text(json.dumps(result,indent=2)+'\\n',encoding='utf-8')
    if result['source_and_distinct_ids'] != [{'source_rows':16,'distinct_encounter_ids':15}]:
        raise AssertionError("Fixture row-count contract changed; inspect fixture and update expected counts deliberately.")
    if len(result['duplicate_ids']) != 1 or result['duplicate_ids'][0]['encounter_id'] != 'E015':
        raise AssertionError("Duplicate detection contract failed.")
    return result

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--db',default=str(Path(__file__).resolve().parents[1]/'fixtures'/'clinic_ops.sqlite'))
    p.add_argument('--output',default=str(Path(__file__).resolve().parents[1]/'reports'))
    a=p.parse_args()
    print(json.dumps(run(a.db,a.output),indent=2))
