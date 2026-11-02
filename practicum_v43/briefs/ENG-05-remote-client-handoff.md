# ENG-05 — Remote client request-to-handoff simulation

**Client:** Fictional healthcare analytics manager  
**Decision:** Can you safely turn an ambiguous request into a reproducible deliverable?  
**Timebox:** 90 minutes.

## Request
A client emails: “Please send the latest monthly readmission and medication adherence dashboard by tomorrow. The numbers do not match last month's report.”

## Required deliverables
1. Clarifying questions and written scope/assumptions.
2. Metric contract for readmission and an adherence proxy.
3. Source-to-output lineage and data-quality plan.
4. Client update explaining what can be confirmed now vs what needs validation.
5. Handoff message with version, limitations, acceptance request and next steps.

## Acceptance criteria
- Ask for metric definitions, population, date window and source systems.
- Distinguish readmission from an unvalidated flag.
- Distinguish adherence proxy (PDC/MPR) from actual ingestion.
- Do not fabricate values when source data are not specified.
- Protect PHI; request minimum necessary access and approved transfer.
