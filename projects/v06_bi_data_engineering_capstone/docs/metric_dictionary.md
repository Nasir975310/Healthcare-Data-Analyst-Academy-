# V06 metric dictionary

- **Encounter count:** distinct encounter IDs in the selected filter context.
- **Distinct patients:** distinct patient IDs with eligible encounters; not the same as encounter count.
- **Mean LOS:** arithmetic mean of encounter-level length of stay in days; interpret with median and distribution.
- **30-day readmission flag proportion:** sum of synthetic flags divided by eligible encounter rows. This is a generated teaching variable, not a validated readmission measure.
- **Medication order lines:** distinct order IDs.
- **Generic documentation percentage:** order lines with generic_documented=1 divided by all eligible order lines × 100. This is a synthetic documentation proxy, not a full prescribing-quality indicator.

Every report must show selected dates, source file version and denominator. Never interpret these artificial data as hospital performance or clinical evidence.
