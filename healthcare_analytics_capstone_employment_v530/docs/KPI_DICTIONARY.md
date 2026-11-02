# KPI dictionary

| KPI | Definition | Grain / caveat |
|---|---|---|
| Patient count | Distinct patient IDs | Dataset-wide |
| Encounter count | Distinct encounter IDs | Includes cancelled encounters |
| Completed encounters | Encounters with status `Completed` | Operational status only |
| Cancelled encounters | Encounters with status `Cancelled` | Not a clinical outcome |
| Medication orders | Count of medication-order IDs | Not proof of dispensing or adherence |
| Unique medications | Distinct medication names | Names are not normalized ingredients |
| Mean systolic BP | Arithmetic mean of systolic observation values | Descriptive; no patient-level adjustment |
| Mean diastolic BP | Arithmetic mean of diastolic observation values | Descriptive; no patient-level adjustment |
| Systolic readings >=140 | Count of systolic observations at/above 140 mmHg | Configurable flag, not a guideline-based control rate |
