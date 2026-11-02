# v5.36.0 QA report

- New module unit tests: 5/5 passed.
- v5.35 employer-evaluation regression tests: 5/5 passed.
- Sample submission scorer: exit code 0; 10/10 checklist items detected.
- Python compilation: passed.
- Interactive roadmap JavaScript syntax (`node --check`): passed.
- Root Academy HTML static parse: passed; no duplicate IDs detected.
- Academy navigation link to v5.36 roadmap: present.
- External integrations: not executed (no job applications, client work, GitHub publication, Power BI Desktop or PostgreSQL deployment).

Note: the Python runtime emitted an `artifact_tool` spreadsheet warmup warning during startup. It did not prevent the new or regression test suites from passing. The scorer is deliberately heuristic and does not execute or validate submitted analysis code.
