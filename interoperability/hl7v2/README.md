# HL7 v2 training fixture

`ADT_A01_synthetic.hl7` is a simplified synthetic HL7 v2.5 admission message. It is provided to practise segment and field reading, not to claim conformance to a hospital's interface specification.

Segments:
- MSH: message header, delimiters, sender/receiver, message type, control ID, processing ID and version.
- EVN: event type and event timestamp.
- PID: patient identification and demographics.
- PV1: patient visit context and patient class/location.

Actual interfaces require a local implementation guide, profile, code tables, acknowledgement handling, error queues, replay controls and security review. Do not assume field positions are universally populated identically across implementations.
