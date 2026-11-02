# KPI dictionary and caveats

| KPI | Definition | Grain / limitation |
|---|---|---|
| Patients | Count of distinct patient IDs | Patient dimension |
| Source encounters | Raw encounter rows | Includes rejected rows |
| Curated encounters | Encounter rows with valid patient FK and date | Curated fact |
| Completed encounters | Curated encounters with status Completed | Operational status only |
| Cancelled encounters | Curated encounters with status Cancelled | Not a clinical outcome |
| Scheduled encounters | Curated encounters with status Scheduled | May not have occurred |
| Medication orders | Count of medication-order IDs in curated fact | Not dispensing or adherence |
| Mean systolic BP | Arithmetic mean of systolic observations | Descriptive, unadjusted |
| Mean diastolic BP | Arithmetic mean of diastolic observations | Descriptive, unadjusted |

All results describe a small synthetic training dataset. BP averages and threshold counts must not be interpreted as diagnosis, hypertension control, guideline compliance or quality-of-care measures.
