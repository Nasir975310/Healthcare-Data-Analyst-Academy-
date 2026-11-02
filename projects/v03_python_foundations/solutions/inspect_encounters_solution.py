"""Worked solution: inspect synthetic encounters using only Python's standard library."""
from pathlib import Path
import csv
from collections import Counter

DATA_FILE = Path(__file__).resolve().parents[3] / "datasets" / "v03_python" / "encounters.csv"

def main():
    with DATA_FILE.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    encounter_types = Counter(row["encounter_type"] for row in rows)
    missing_sbp = sum(row["systolic_bp"] == "" for row in rows)
    dates = sorted(row["admission_date"] for row in rows if row["admission_date"])

    print(f"Encounter rows: {len(rows)}")
    print("Encounter type counts:")
    for encounter_type, count in sorted(encounter_types.items()):
        print(f"  {encounter_type}: {count}")
    print(f"Missing SBP: {missing_sbp}")
    print(f"Nonmissing SBP: {len(rows) - missing_sbp}")
    print(f"Date range: {dates[0]} to {dates[-1]}")

if __name__ == "__main__":
    main()
