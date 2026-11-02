from pathlib import Path
import pandas as pd
BASE=Path(__file__).resolve().parents[1]
D=BASE/"data"; O=BASE/"reports"
O.mkdir(exist_ok=True)
patients=pd.read_csv(D/"patients.csv")
enc=pd.read_csv(D/"encounters.csv",parse_dates=["admission_date"])
orders=pd.read_csv(D/"medication_orders.csv")
assert patients.patient_id.is_unique and enc.encounter_id.is_unique and orders.order_id.is_unique
assert set(enc.patient_id).issubset(set(patients.patient_id))
assert set(orders.encounter_id).issubset(set(enc.encounter_id))
# Aggregate each fact at its own grain before combining.
dept=(enc.groupby(["department","site"],as_index=False)
      .agg(encounters=("encounter_id","nunique"),
           patients=("patient_id","nunique"),
           mean_los=("length_of_stay_days","mean"),
           median_los=("length_of_stay_days","median"),
           synthetic_readmission_flag_pct=("readmission_30d","mean")))
dept["synthetic_readmission_flag_pct"]*=100
drug=(orders.groupby("drug_class",as_index=False)
      .agg(order_lines=("order_id","nunique"),
           generic_documented=("generic_documented","sum")))
drug["generic_documentation_pct"]=100*drug.generic_documented/drug.order_lines
dept.to_csv(O/"department_mart.csv",index=False)
drug.to_csv(O/"medication_mart.csv",index=False)
(O/"validation.txt").write_text(
    f"patients={len(patients)}\nencounters={len(enc)}\norders={len(orders)}\n"
    f"unmatched_encounter_patients={len(set(enc.patient_id)-set(patients.patient_id))}\n"
    f"unmatched_order_encounters={len(set(orders.encounter_id)-set(enc.encounter_id))}\n"
    f"department_encounters_reconciled={int(dept.encounters.sum())}\n"
    f"medication_order_lines_reconciled={int(drug.order_lines.sum())}\n"
    "All records are synthetic; no clinical or hospital performance inference is supported.\n")
print((O/"validation.txt").read_text())
