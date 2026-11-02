from pathlib import Path
import sqlite3

def build(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()
    rows = [
        ("E001","P001","Cardiology","2026-10-05","completed",22,"SYS-A"),
        ("E002","P002","General Medicine","2026-10-05","completed",35,"SYS-A"),
        ("E003","P003","Cardiology","2026-10-06","completed",18,"SYS-A"),
        ("E004","P004","General Medicine","2026-10-06","cancelled",None,"SYS-A"),
        ("E005","P005","Orthopaedics","2026-10-07","completed",41,"SYS-B"),
        ("E006","P006","Cardiology","2026-10-12","no_show",None,"SYS-A"),
        ("E007","P007","Orthopaedics","2026-10-13","completed",29,"SYS-B"),
        ("E008","P008","General Medicine","2026-10-13","completed",None,"SYS-A"),
        ("E009","P009","Cardiology","2026-10-14","completed",24,"SYS-A"),
        ("E010","P010","General Medicine","2026-10-14","completed",-4,"SYS-A"),
        ("E011","P011","Orthopaedics","2026-10-15","completed",33,"SYS-B"),
        ("E012","P012",None,"2026-10-15","completed",27,"SYS-B"),
        ("E013","P013","Cardiology","2026-10-19","completed",20,"SYS-A"),
        ("E014","P014","General Medicine","2026-10-20","completed",31,"SYS-A"),
        ("E015","P015","Orthopaedics","2026-10-20","completed",26,"SYS-B"),
        ("E015","P015","Orthopaedics","2026-10-20","completed",26,"SYS-B"),
    ]
    with sqlite3.connect(path) as con:
        con.execute('CREATE TABLE encounters(encounter_id TEXT, patient_id TEXT, department TEXT, encounter_date TEXT, status TEXT, wait_minutes REAL, source_system TEXT)')
        con.executemany("INSERT INTO encounters VALUES (?,?,?,?,?,?,?)", rows)
    return len(rows)

if __name__ == "__main__":
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument("--output", default=str(Path(__file__).resolve().parents[1]/"fixtures"/"clinic_ops.sqlite"))
    args=parser.parse_args()
    print(f"Created synthetic fixture with {build(args.output)} rows at {args.output}")
