"""Profile the bundled synthetic encounter dataset."""
from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "data" / "raw" / "synthetic_encounters.csv"
OUTPUT = ROOT / "reports" / "generated" / "profile.json"

def build_profile() -> dict:
    df = pd.read_csv(INPUT)
    result = {
        "dataset": INPUT.name,
        "row_count": int(len(df)),
        "column_count": int(len(df.columns)),
        "duplicate_encounter_ids": int(df["encounter_id"].duplicated().sum()),
        "missing_by_column": {k: int(v) for k, v in df.isna().sum().items()},
        "unique_patients": int(df["patient_token"].nunique()),
        "synthetic_data": True,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    print(json.dumps(build_profile(), indent=2))
