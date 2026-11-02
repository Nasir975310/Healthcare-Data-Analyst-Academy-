# Healthcare Analytics Portfolio Release Gate

A project may be marked **portfolio ready** only when all critical gates are met.

## A. Scope and metric validity
- [ ] Business/clinical question is explicit and bounded.
- [ ] Intended audience and decision context are identified.
- [ ] Unit of analysis and table grain are documented.
- [ ] Inclusion, exclusion, time window and denominator rules are explicit.
- [ ] Numerator/denominator and missing-data handling are documented.
- [ ] Orders, administrations, dispensing and adherence are not conflated.
- [ ] Association is not described as causation without a valid causal design.

## B. Data governance and safety
- [ ] Data source, rights/authorisation and provenance are documented.
- [ ] Synthetic/public/authorised status is explicit.
- [ ] No PHI, patient identifiers, confidential employer data or credentials are published.
- [ ] Small-cell disclosure and re-identification risks are considered.
- [ ] Repository visibility and licence are intentional.
- [ ] Raw data are excluded if sharing is not authorised.

## C. Reproducibility
- [ ] README has setup and exact run instructions.
- [ ] Runtime and dependencies are pinned or constrained.
- [ ] Input files and expected schemas are listed.
- [ ] Data dictionary includes field, type, unit, definition, allowed values and null meaning.
- [ ] Random seeds are set where stochastic methods are used.
- [ ] Scripts/queries run from a clean checkout or environment.
- [ ] Outputs can be regenerated and are not hand-edited without disclosure.
- [ ] Execution logs or QA evidence are retained without sensitive data.

## D. Technical quality
- [ ] Primary keys and expected grain are tested.
- [ ] Duplicate, null, range, chronology and referential integrity checks are performed where relevant.
- [ ] Joins are checked for row multiplication and denominator changes.
- [ ] SQL is parameterised where user input is involved.
- [ ] Statistical assumptions and model diagnostics are checked.
- [ ] Dashboard filters, date logic and totals reconcile to source queries.
- [ ] Error handling and failure modes are documented.

## E. Interpretation and communication
- [ ] Results include units, denominators and uncertainty where appropriate.
- [ ] Findings are distinguished from recommendations.
- [ ] Limitations, bias, missingness and generalisability are explicit.
- [ ] No unsupported clinical recommendations are made.
- [ ] Executive summary is concise and audience-appropriate.
- [ ] Visuals have clear titles, labels, units and source notes.

## F. Release
- [ ] Code review completed.
- [ ] Automated checks pass; known warnings are explained.
- [ ] No obvious secrets in working tree or Git history.
- [ ] Licence/sharing statement is present.
- [ ] Release tag/version and change log are recorded.
- [ ] A second person can reproduce at least one key result.
- [ ] Portfolio case study clearly labels training/synthetic work.

**Critical fail:** PHI or credentials exposed, unlicensed data shared, materially invalid metric, unrepeatable key result, or a clinical claim unsupported by study design. A critical fail blocks publication regardless of numeric score.
