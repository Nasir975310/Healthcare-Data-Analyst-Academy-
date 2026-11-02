from pathlib import Path
import pandas as pd
BASE = Path(__file__).resolve().parents[1]
df = pd.read_csv(BASE / "fixtures" / "encounters.csv", parse_dates=["admit_date", "discharge_date"])
assert df["encounter_id"].is_unique, "Encounter key must be unique"
assert df["patient_id"].notna().all(), "Patient identifier missing"
assert (df["discharge_date"] >= df["admit_date"]).all(), "Negative length of stay"
active = df[(df.order_status == "Active") & (df.drug_class == "Antihypertensive")]
print("Encounter rows:", len(df))
print("Unique patients:", df.patient_id.nunique())
print("Active antihypertensive patient count:", active.patient_id.nunique())
print("\\nDepartment summary:")
print(df.groupby("department").agg(encounters=("encounter_id","count"), patients=("patient_id","nunique")))
