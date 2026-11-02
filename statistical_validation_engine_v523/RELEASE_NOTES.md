# Release 5.23.0 — Advanced Clinical Research & Statistical Validation

A validation layer that complements v5.21 statistical execution and v5.22 integrated reporting. Includes group-level normality and variance diagnostics, linear model residual/heteroscedasticity/influence/multicollinearity checks, HC3 robust standard errors, seeded bootstrap mean intervals, and explicit multiple-testing corrections. This release reports diagnostics; it does not automatically certify models or select tests.

## QA summary
- v5.23 tests: 8 passed.
- Synthetic end-to-end run: 20 records; one group diagnostic, one bootstrap interval, one linear regression diagnostic set and one multiplicity family generated.
- Regression suites: v5.22 (6), v5.21 (8), v5.19 (7), v5.18 (5), v5.17 (5), v5.15 (5) passed.
- Repository checks: 109 Python files compiled, 253 JSON files parsed, 54 JavaScript files syntax-checked; no errors, duplicate HTML IDs or missing script assets.
