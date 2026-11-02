# Metric governance and dashboard design

Every published metric needs an owner, business definition, numerator, denominator, inclusion/exclusion rules, grain, refresh cadence, source, known limitations and validation query. Version definitions; do not silently change a KPI.

## Dashboard audiences
- Executive: encounter volume, unique patients, IPD share, charges (label as charges, not revenue), trend and variance.
- Clinical operations: department workload, IPD length of stay, transfer status, monthly volume.
- Pharmacy: medication-review encounters, activity trend and workload; this fixture has no medication-level exposure or outcome data.

## Release gate
- Reconcile row counts and totals to source SQL.
- Test slicers, date boundaries, blanks, zero denominators and multiple selections.
- Test RLS with representative users and confirm export behaviour.
- Record refresh timestamp, source version and data-quality exceptions.
- Add accessible titles, units, definitions and non-colour-only status cues.

All fixture data is synthetic and unsuitable for clinical inference or operational decisions.
