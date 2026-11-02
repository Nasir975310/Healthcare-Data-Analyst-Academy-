# Metric definitions and denominator contract

- **Record count:** number of non-empty data rows after CSV parsing. Denominator: all parsed rows.
- **Unique patient tokens:** count of distinct nonblank `patient_id` values. This is a distinct count, not an encounter count.
- **Missingness:** blank/null-like cells divided by all cells in the corresponding field. Denominator: number of parsed rows.
- **Numeric mean/median:** descriptive statistic of parseable numeric values in a selected field. Denominator: number of parseable numeric values; invalid/blank values excluded and should be reported.
- **Category frequency:** count of rows in each category. Denominator: all parsed rows, including blank category as `(missing)`.

These definitions are generic descriptive metrics. Adapt and approve a metric contract before operational or clinical use.
