# Healthcare analytics warehouse architecture

```mermaid
flowchart LR
  EHR[EHR / ADT] --> I[Interface / API ingestion]
  P[Pharmacy / Medication system] --> I
  L[Laboratory system] --> I
  I --> R[Immutable raw / landing]
  R --> S[Staging and schema validation]
  S --> N[Clinical standardisation and terminology mapping]
  N --> Q[Quality quarantine and reconciliation]
  N --> W[Curated warehouse]
  Q --> W
  W --> M[Dimensional marts]
  M --> B[BI / research analytics]
  G[Identity, access, audit, lineage, retention] --- I
  G --- R
  G --- W
  G --- B
```

## Design decisions
- Operational systems are optimised for care delivery and transactions; analytics workloads should not overload them.
- Preserve immutable source payloads under governed retention and access rules.
- Record source system, source resource/message ID, version, ingestion timestamp and transformation version.
- Separate structural validation from semantic clinical validation.
- Maintain an explicit quarantine/review path; do not silently discard invalid records.
- Define fact-table grain before joining: encounter, medication request/order and observation are separate grains.
- Use conformed patient, date, department and terminology dimensions where appropriate.
- Apply least privilege, audit logging and approved retention policies at each layer.
- Reconcile source, staged, quarantined and curated counts for each pipeline run.
