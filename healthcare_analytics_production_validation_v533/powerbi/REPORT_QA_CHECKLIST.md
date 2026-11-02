# Power BI report QA checklist

- [ ] Model grain documented for every fact table.
- [ ] Relationships are one-to-many, dimension-to-fact, single direction by default.
- [ ] No many-to-many or ambiguous paths without documented justification.
- [ ] Date table marked; date relationships tested at month/year boundaries.
- [ ] DAX measures reconcile to SQL under identical filters.
- [ ] Distinct patient count is not confused with encounter count.
- [ ] Medication orders are not described as dispensing or adherence.
- [ ] Every chart has title, unit, date window and denominator where relevant.
- [ ] Tooltips and slicers do not expose identifiers.
- [ ] Keyboard navigation, contrast, alt text and readable labels checked.
- [ ] Refresh failure behavior and last successful refresh visible.
- [ ] Performance Analyzer evidence captured.
- [ ] Exported PDF/CSV does not leak row-level sensitive data.
