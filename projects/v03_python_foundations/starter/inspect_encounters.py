"""Starter: inspect a synthetic encounter CSV.

Run from the project folder:
python starter/inspect_encounters.py
"""
from pathlib import Path
import csv

DATA_FILE = Path(__file__).resolve().parents[3] / "datasets" / "v03_python" / "encounters.csv"

def main():
    with DATA_FILE.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    print("Rows:", len(rows))
    print("Columns:", reader.fieldnames)
    # TODO 1: count encounters by encounter_type.
    # TODO 2: count missing systolic_bp values (empty string).
    # TODO 3: print the earliest and latest admission_date.

if __name__ == "__main__":
    main()
