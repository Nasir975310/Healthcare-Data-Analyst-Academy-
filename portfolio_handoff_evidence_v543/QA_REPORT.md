# v5.43.0 QA report

- New handoff-gate tests: **6/6 passed**.
- v5.42 publication module tests: **4/4 passed** (run from its module root, as required by its import layout).
- Exported synthetic outpatient sample tests: **5/5 passed**.
- Exported synthetic outpatient pipeline: **exit code 0**; 24 raw rows, 1 duplicate removed, 20 eligible completed encounters, 18 valid wait observations.
- Evidence-template behavior: **PENDING_EVIDENCE**, 17 required fields missing; expected exit code 2. This confirms blank template is not misreported as PASS.
- Python compilation for the new and publication modules: passed.
- External GitHub publication, live Actions execution, user clean-clone reproduction and independent review: **NOT_RUN**.
- Limitations: the gate validates supplied fields and internal consistency; it does not call GitHub or authenticate the evidence or reviewer.
