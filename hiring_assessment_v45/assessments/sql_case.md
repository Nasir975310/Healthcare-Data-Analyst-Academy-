# Stage 2 — SQL technical case (35 minutes)

A synthetic hospital has tables:
- `encounters(encounter_id PRIMARY KEY, patient_id, department, admission_date, discharge_date, los_days)`
- `orders(order_id PRIMARY KEY, encounter_id, drug_class, order_date, quantity, unit_cost)`

Tasks:
1. Return encounter count and unique patient count by department.
2. Return medication-order count and estimated order value by department.
3. Find orders with no matching encounter.
4. Find encounters without any order.
5. Explain why joining raw orders to encounters before calculating average LOS can change the result.
6. Propose a safe query pattern that pre-aggregates order metrics by encounter before joining.
7. State at least four validation queries/checks.

**Scoring:** grain and correctness 8; join integrity 4; aggregation 4; validation 4.
