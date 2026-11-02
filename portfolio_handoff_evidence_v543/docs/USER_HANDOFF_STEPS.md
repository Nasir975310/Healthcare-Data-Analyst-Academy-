# Portfolio handoff: user-side execution

This procedure is intentionally separate from the Academy's synthetic fixture tests. Run it only after deciding the intended GitHub destination and completing the privacy/provenance review.

1. Open the exported repository folder from `github_portfolio_publication_v542/sample_export/` (or the final export you personally reviewed).
2. Create a new, dedicated GitHub repository. Do not reuse an unrelated repository. Choose public/private visibility deliberately.
3. From that folder, run `git init -b main`, `git add -A`, `git diff --cached --check`, inspect `git diff --cached`, commit, add the new remote, and push. Do not commit credentials or raw patient-level data.
4. In GitHub, open **Actions** and record the actual workflow run URL, run ID, conclusion and commit SHA. A workflow file existing locally is not evidence that CI ran.
5. In a separate temporary directory, clone the remote URL. Verify the clone's HEAD SHA matches the pushed commit. Run the exact README test command and save the complete terminal output.
6. Ask an independent reviewer to inspect the public/private repository contents, data provenance, privacy risk and stated limitations. Record their actual review; do not self-label this independent review.
7. Copy actual values into `templates/HANDOFF_EVIDENCE.json`, save as `evidence/my_handoff_evidence.json`, then run:

```bash
python portfolio_handoff_evidence_v543/src/handoff_gate.py \
  --evidence portfolio_handoff_evidence_v543/evidence/my_handoff_evidence.json \
  --out portfolio_handoff_evidence_v543/evidence/my_handoff_gate_report.json
```

Exit code 0 means the supplied fields are internally consistent. Exit code 2 means evidence is incomplete or inconsistent. The tool does not contact GitHub or authenticate the claims; inspect the URLs and artifacts yourself.
