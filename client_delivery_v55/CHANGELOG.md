# v5.5.0 — Healthcare Analytics Client Delivery & Evidence Pack

- Added an interactive client-delivery workspace with CSV profiling, artifact inventory fields, 12 handoff QA attestations, findings/limitations and recipient details.
- Added browser-local evidence JSON and standalone handoff HTML export; source CSV SHA-256 is computed from the actual loaded text where Web Crypto is available.
- Added a Python delivery-pack builder that copies supplied source/report/dashboard/dictionary/metric-contract artifacts, generates a dataset profile, creates an artifact manifest with SHA-256 checksums, and packages a ZIP.
- Added Linux and Windows PowerShell instructions and a synthetic example delivery pack.
- The checklist is an attestation, not independent verification or legal/privacy certification.
