from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "reports" / "outputs"
OUT.mkdir(parents=True, exist_ok=True)

patients = pd.read_csv(DATA / "patients.csv")
enc = pd.read_csv(DATA / "encounters.csv", parse_dates=["admission_date", "discharge_date"])
med = pd.read_csv(DATA / "medication_orders.csv")
lab = pd.read_csv(DATA / "laboratory_results.csv")

assert patients.patient_id.is_unique
assert enc.encounter_id.is_unique
assert med.order_id.is_unique
assert lab.result_id.is_unique
assert set(enc.patient_id).issubset(set(patients.patient_id))
assert set(med.encounter_id).issubset(set(enc.encounter_id))
assert set(lab.encounter_id).issubset(set(enc.encounter_id))
assert (enc.discharge_date >= enc.admission_date).all()

enc_summary = enc.groupby("department").agg(
    encounters=("encounter_id","nunique"),
    distinct_patients=("patient_id","nunique"),
    mean_los_days=("length_of_stay_days","mean"),
    median_los_days=("length_of_stay_days","median")
).reset_index()
enc_summary.to_csv(OUT / "department_summary.csv", index=False)

med_summary = med.groupby("drug_class").agg(
    order_lines=("order_id","nunique"),
    generic_documented=("generic_name_documented","sum")
).reset_index()
med_summary["generic_documentation_pct"] = 100*med_summary.generic_documented/med_summary.order_lines
med_summary["order_share_pct"] = 100*med_summary.order_lines/med_summary.order_lines.sum()
med_summary.to_csv(OUT / "medication_class_summary.csv", index=False)

lab_summary = lab.groupby(["analyte","unit","status"]).agg(
    result_rows=("result_id","nunique"), mean_value=("value","mean"), median_value=("value","median")
).reset_index()
lab_summary.to_csv(OUT / "laboratory_profile.csv", index=False)

validation = [
    f"patients={len(patients)}",
    f"encounters={len(enc)}",
    f"medication_order_lines={len(med)}",
    f"laboratory_result_rows={len(lab)}",
    f"encounter_patients_unmatched={len(set(enc.patient_id)-set(patients.patient_id))}",
    f"medication_encounters_unmatched={len(set(med.encounter_id)-set(enc.encounter_id))}",
    f"lab_encounters_unmatched={len(set(lab.encounter_id)-set(enc.encounter_id))}",
    "all_primary_keys_unique=True",
    "all_discharge_dates_on_or_after_admission=True",
    "No clinical inference or quality ranking is supported by these synthetic data."
]
(OUT / "validation.txt").write_text("\n".join(validation)+"\n")
print("\n".join(validation))
