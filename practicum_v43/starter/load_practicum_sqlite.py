"""Build a local SQLite database from synthetic practicum CSVs.
Usage: python load_practicum_sqlite.py
"""
from pathlib import Path
import sqlite3
import pandas as pd
HERE=Path(__file__).resolve().parent
DATA=HERE.parent/"data"
DB=HERE.parent/"practicum_training.sqlite"
tables={
 "encounters":DATA/"hospital_encounters_raw.csv",
 "due_cohort":DATA/"antihypertensive_due_raw.csv",
 "pv_cases":DATA/"pv_cases_raw.csv",
 "medication_orders":DATA/"medication_orders_raw.csv",
}
with sqlite3.connect(DB) as con:
    for table,path in tables.items():
        pd.read_csv(path).to_sql(table,con,if_exists="replace",index=False)
    con.execute("CREATE INDEX IF NOT EXISTS idx_orders_encounter ON medication_orders(encounter_id)")
    con.execute("CREATE INDEX IF NOT EXISTS idx_encounters_id ON encounters(encounter_id)")
    con.commit()
    print("SQLite database:",DB)
    for table in tables:
        print(table,con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])
