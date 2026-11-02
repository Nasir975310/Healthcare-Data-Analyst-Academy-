# Reference run — synthetic fixture

The packaged input contains 24 rows:
- 1 duplicate encounter row removed; 23 unique encounter IDs remain.
- 20 eligible completed encounter records (completed status, valid date, nonblank department).
- 18 of those have valid nonnegative wait values for the mean-wait metric.
- Cardiology: 7 eligible completed encounters; valid wait n=7; mean 21.29 minutes.
- General Medicine: 7 eligible completed encounters; valid wait n=5; mean 32.60 minutes.
- Orthopaedics: 6 eligible completed encounters; valid wait n=6; mean 33.67 minutes.

These figures are reproducible from the included synthetic CSV. They are not hospital performance benchmarks.
