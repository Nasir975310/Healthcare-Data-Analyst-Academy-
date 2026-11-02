# Portfolio Quality Gate & Reproducibility Toolkit

Run the repository audit from the root of a portfolio repository:

```bash
python /path/to/portfolio_quality/scripts/audit_portfolio.py .
```

Strict review mode (returns exit code 2 below 85/100 or when configured secret/PHI heuristics trigger):

```bash
python /path/to/portfolio_quality/scripts/audit_portfolio.py . --strict --output portfolio_audit.json
```

The report is a triage aid. It checks documentation cues, environment files, data dictionary, QA artefacts, licence/sharing terms, provenance disclosure, analytical files and a few high-signal secret/PHI patterns. It does **not** execute project code, inspect database permissions, establish that data are de-identified, or certify security/privacy/regulatory compliance. False positives and false negatives are possible.

## Recommended release sequence
1. Run the audit on a copy or branch of the repository.
2. Resolve documentation and reproducibility gaps.
3. Execute the actual project tests and reference queries independently.
4. Manually inspect data, outputs, credentials, git history and repository visibility.
5. Review clinical/statistical interpretation and limitations.
6. Ask a peer to reproduce the headline result from a clean environment.
7. Tag and publish only after the release checklist is signed off.


## Interactive review checklist
The Academy sidebar includes **Portfolio quality gate & reproducibility**. Its checklist is stored in localStorage and can be exported as Markdown or a v3.6 JSON backup. Checklist completion does not automatically certify a project; the user must collect and review evidence.
