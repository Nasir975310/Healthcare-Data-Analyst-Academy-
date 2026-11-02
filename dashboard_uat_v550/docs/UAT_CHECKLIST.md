# Dashboard UAT checklist

Record the date, OS/browser version, and outcome. Do not include patient identifiers or private workstation details.

- [ ] Page loads without a blank screen or console-breaking error.
- [ ] Page loads and the filtered-record KPI is greater than zero.
- [ ] Paired-SBP KPI is greater than zero.
- [ ] Selecting a drug class changes the filtered record count.
- [ ] Reset filters restores the initial count.
- [ ] Selecting “At least one recorded” comorbidity filter updates the view without error.
- [ ] CSV export downloads `filtered_synthetic_hypertension_records.csv`.
- [ ] Exported CSV opens and retains headers and quoted fields.
- [ ] Dashboard warning clearly identifies the data as synthetic.
- [ ] No real patient data or identifying information is present in screenshots or exports.

## Defect report
- Test / filter:
- Expected:
- Actual:
- Reproduction steps:
- Browser and version:
- Severity: Blocker / High / Medium / Low
- Evidence filename (sanitized):
