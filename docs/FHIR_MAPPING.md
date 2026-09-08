# FHIR R4 mapping boundary

Target **R4 4.0.1** per SRS A-01/BR-PLT-05-01. M0 has mapping documents only: no `/fhir` endpoints, no resource export, no full FHIR server or validation pass. M5 introduces an isolated adapter over authorized domain DTOs; never rename domain columns to avoid thinking through conversion

| Domain | Target R4 resource / subset | Validation required in M5 |
|---|---|---|
| Party + Patient + HN identifier | Patient: id, identifier, name, birthDate, active | correct identifier system, date, data types; only authorized identity subset |
| Encounter | Encounter: id, status, class, subject, period | status conversion, AMB coding, valid Patient reference |
| Observation | Observation: status, code, subject, encounter, effectiveDateTime, valueQuantity/unit or supported typed value, referenceRange | supported code/unit pairing, exactly appropriate value type, bounded references |
| Lab Order | ServiceRequest: status, intent=order, code, subject, encounter, authoredOn, requester | lab supported fields only; no unsupported search claims |
| Medication Order | MedicationRequest: status, intent=order, medicationCodeableConcept, subject, encounter, authoredOn, dosageInstruction subset | supported structured dosage; no synthetic local drug code presented as TMT |

| Internal Encounter status | Proposed R4 Encounter.status | Handling |
|---|---|---|
| planned | planned | direct |
| in_progress | in-progress | underscore conversion is explicit |
| on_hold | onleave | only if local meaning matches temporary leave; otherwise adapter must reject pending ADR |
| discharged | finished | FHIR clinical visit finished; billing still open internally, not forced completed |
| completed | finished | local clinical and financial tasks finished |
| cancelled | cancelled | direct |
| entered_in_error | entered-in-error | direct |
| discontinued | unsupported | do not guess; fail export until a supported mapping is agreed |

R4 Order status mappings differ by resource: ServiceRequest active/on-hold/revoked/completed/entered-in-error; draft supported where appropriate. MedicationRequest has cancelled/stopped distinctions. Adapter must define action+status mappings explicitly before export, not copy internal enum strings wholesale

## Supported operations at v0.1

| Operation | State |
|---|---|
| Documentation mapping | AVAILABLE |
| Patient/Encounter/Observation/ServiceRequest/MedicationRequest export | NOT_IMPLEMENTED (M5) |
| FHIR create/update/delete/search/history, subscriptions, SMART | OUT_OF_SCOPE |
| CapabilityStatement | NOT_IMPLEMENTED; if added list only actual endpoints |
| R5 / SIL-TH / MoPH / TH Core / government submission | OUT_OF_SCOPE |

## Validation plan

Pin resource definitions/schema/validator version to R4 4.0.1. Validate positive exports and negative fixtures (bad code, reference, required field, unsupported status). Structural JSON parsing alone is insufficient; record supported schema/profile checks and unresolved terminology validation separately. Validate referential coherence, security projection, and audit every export. HAPI is a comparative validator reference, not a required Java service in this Python application

Primary standards reference: [FHIR R4](https://hl7.org/fhir/R4/), [Encounter](https://hl7.org/fhir/R4/encounter.html), [Observation](https://hl7.org/fhir/R4/observation.html). These mappings remain a reviewed proposal until M5 validation evidence exists
