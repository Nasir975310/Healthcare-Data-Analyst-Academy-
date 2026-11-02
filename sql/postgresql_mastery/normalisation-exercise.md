# Normalisation exercise

## Declare the grain
- Encounter: one row per hospital encounter.
- Drug: one row per drug/route combination in this training model.
- Medication order: one row per medication order.
- Department: one row per department.

## 1NF
Each field contains one atomic value. Repeating columns such as drug_1, drug_2 and drug_3 become medication-order rows.

## 2NF
Every non-key attribute depends on the whole candidate key. Although this schema uses surrogate keys, identify partial dependencies in a composite-key alternative.

## 3NF
Non-key attributes should not depend transitively on another non-key attribute. Department name belongs in departments; drug class and route belong in the drug reference table.

## Deliverable
Draw the original grain, proposed entities, PK/FK relationships, and three update anomalies prevented by normalisation. Explain why a reporting star schema may intentionally denormalise dimensions for analytics.
