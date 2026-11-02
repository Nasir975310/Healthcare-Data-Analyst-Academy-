"""Load the synthetic CSV into a local SQLite training database."""
from pathlib import Path
import csv
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "raw" / "synthetic_encounters.csv"
DB_PATH = ROOT / "data" / "health_analytics.sqlite"

def main():
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS encounters (
            encounter_id TEXT PRIMARY KEY, patient_token TEXT NOT NULL,
            admission_date TEXT NOT NULL, department TEXT NOT NULL,
            length_of_stay_days INTEGER NOT NULL, discharge_disposition TEXT,
            age_band TEXT NOT NULL)""")
        conn.execute("DELETE FROM encounters")
        conn.executemany("""INSERT INTO encounters VALUES
            (:encounter_id,:patient_token,:admission_date,:department,
             :length_of_stay_days,:discharge_disposition,:age_band)""",
            [{**r, "length_of_stay_days": int(r["length_of_stay_days"])} for r in rows])
        count = conn.execute("SELECT COUNT(*) FROM encounters").fetchone()[0]
    print(f"Loaded {count} synthetic encounters into {DB_PATH}")
if __name__ == "__main__":
    main()
