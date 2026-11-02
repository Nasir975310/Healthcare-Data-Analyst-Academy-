# Power BI report blueprint — Hospital Operations & Medication Utilisation

## Audience and decision
Hospital operations leadership and pharmacy analytics stakeholders. The report supports descriptive review of synthetic encounter flow, length of stay, supplied readmission flags and medication-order mix. It is not a clinical decision-support tool.

## Page 1 — Executive overview
- KPI cards: Encounter Count; Mean Length of Stay (days); Supplied Readmission Flag Rate; Medication Order Count; Ordered Quantity.
- Bar chart: Encounter count by department.
- Bar chart: Mean LOS by department (same scale and units).
- Trend: encounters by admission month. Use DimDate[year_month], sorted by month_start.
- Slicers: admission month, department, payer.
- Footer note: synthetic dataset; readmission flag supplied and not independently validated.

## Page 2 — Medication utilisation
- KPI cards: medication order count; ordered quantity; synthetic order value.
- Bar chart: order count by therapeutic class.
- Stacked bar: order status by pharmacy location.
- Matrix: drug name × order status with order count and ordered quantity.
- Slicers: order month, department, therapeutic class, route.
- Caveat: an order is not proof of dispensing, administration, adherence or appropriateness.

## Page 3 — Data quality
- Cards: missing unit cost; blank therapeutic class; orphan encounter references.
- Table of exception rows with order_id, encounter_key, drug, status and flags.
- Duplicate candidate review should be a separate analysis based on a documented business key; do not auto-delete.
- Show source row counts before and after every transformation.

## Interaction and usability
- Keep slicers page-specific unless a shared selection is intentionally synced.
- Use drill-through from department to encounter detail only when identifiers are safe to display; training data is synthetic.
- Add a Reset filters button/bookmark.
- Use descriptive titles, units, data refresh timestamp and definitions.
- Do not use pie charts for many therapeutic classes; use sorted bars.
- Avoid red/green semantics for clinical quality without a defined threshold and clinical owner.

## Validation before handoff
1. Confirm one row per DimEncounter key and FactEncounterMetrics key.
2. Confirm every DimDrug key is unique.
3. Confirm relationship cardinality and filter direction.
4. Reconcile the headline counts with `model_reference_checks.json`.
5. Test each slicer against all affected visuals and verify denominator behaviour.
6. Check totals after cross-filtering to avoid duplicated encounter measures.
7. Validate report accessibility, contrast, tab order, alt text and mobile layout.
