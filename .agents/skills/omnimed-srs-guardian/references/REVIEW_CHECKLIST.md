# OmniMed SRS Guardian — Review Checklist

This checklist is used by the read-only `omnimed-srs-guardian` skill.

It supplements:
- `AGENTS.md`
- `docs/POC_CONTRACT.md`
- the current task contract
- selected SRS excerpts
- `docs/REQUIREMENT_TRACE.md`

It does NOT create new requirements.

If a checklist item is not applicable to the current task, mark it `N/A`.
If the source documents do not provide enough evidence, return `UNCERTAIN`.
Never infer a requirement merely because it is listed in this checklist.

---

# 1. Scope and Authority

- [ ] Current implementation matches exactly one approved task contract.
- [ ] No unrelated feature was added.
- [ ] No M1–M5 capability is claimed complete based only on M0 infrastructure.
- [ ] No out-of-scope module was introduced.
- [ ] No external reference overrode OmniMed SRS semantics.
- [ ] Any architecture/invariant change has an approved ADR or is blocked.
- [ ] Requirement IDs cited by the implementation exist in the selected SRS source.
- [ ] UI/mockup identifiers are not treated as authoritative SRS requirements.

FAIL if:
- implementation silently expands scope;
- external framework semantics replace SRS semantics;
- unsupported functionality is claimed implemented.

---

# 2. Party / Patient

Apply when Party, Patient, PatientIdentifier or demographic data changes.

- [ ] Patient identity follows the selected OmniMed Party/Patient model.
- [ ] PatientIdentifier belongs to the correct patient/tenant.
- [ ] HN uniqueness follows the task contract.
- [ ] Identifier generation is safe under concurrent creation if required by the task.
- [ ] Cross-tenant patient references are impossible at the database boundary where required.
- [ ] No real patient data exists in fixtures, seeds or screenshots.
- [ ] No Thai citizen ID from a real person is present.
- [ ] Patient data is not duplicated into unrelated module-owned tables.

---

# 3. Encounter

Apply when Encounter behavior changes.

- [ ] Encounter belongs to the correct Patient.
- [ ] Encounter belongs to the correct tenant.
- [ ] Encounter lifecycle matches the selected POC/SRS rules.
- [ ] Clinical measurements are not added as convenience Encounter columns.
- [ ] Encounter history is not destroyed through hard delete.
- [ ] Orders created in the encounter reference that encounter.
- [ ] Cross-tenant Patient → Encounter relationships are prevented.

Examples of suspicious schema:

`encounter.weight_kg`
`encounter.temperature_c`
`encounter.systolic_bp`

These should trigger review against Observation semantics.

---

# 4. Observation

Apply to triage, vital signs, laboratory results or measured clinical data.

- [ ] Measured clinical values use Observation.
- [ ] Observation identifies its Patient/Encounter as required.
- [ ] Value type is represented correctly.
- [ ] Unit is explicit when required.
- [ ] Timestamp/context is preserved.
- [ ] Laboratory result is not stored as an arbitrary Encounter column.
- [ ] Historical observations are not silently overwritten.
- [ ] Tenant isolation is preserved.

Do NOT demand fields that are not required by the current selected SRS/task.

---

# 5. Orders / CPOE

Apply whenever Order changes.

- [ ] Every clinical Order belongs to an Encounter.
- [ ] Order type follows the supported POC subset.
- [ ] Existing Order payload/history is not destructively edited.
- [ ] Revision preserves relationship to the previous order when required.
- [ ] Discontinue/cancel does not masquerade as deletion.
- [ ] Medication and laboratory orders do not create incompatible duplicate order roots.
- [ ] Catalog reference is valid for the order.
- [ ] Actor/time provenance is retained as required.

FAIL if implementation performs an in-place destructive update where
the selected SRS requires revision/history preservation.

---

# 6. CatalogItem

Apply when orderable/billable catalog behavior changes.

- [ ] CatalogItem remains the shared catalog abstraction required by the POC.
- [ ] Drug/lab items are not unnecessarily implemented as independent incompatible catalogs.
- [ ] Orderable/billable semantics match selected requirements.
- [ ] External coding systems are not invented when source mapping is unavailable.
- [ ] Catalog changes do not introduce unrelated inventory/procurement scope.

---

# 7. Laboratory

Apply to Lab Order, worklist and result tasks.

- [ ] Lab receives an appropriate supported Order.
- [ ] Worklist exposes only information required for the lab workflow.
- [ ] Result lifecycle matches the current task contract.
- [ ] Measured lab results become Observations where required.
- [ ] Result provenance is retained.
- [ ] Lab role cannot gain unrelated administrative/financial access.
- [ ] No analyzer integration is introduced in the POC.

---

# 8. Pharmacy

Apply to medication/dispensing tasks.

- [ ] Pharmacy worklist derives from supported medication orders.
- [ ] Dispense references the correct order/patient/encounter.
- [ ] Dispense does not silently rewrite the physician's original order.
- [ ] Actor/time provenance is retained.
- [ ] Charge generation follows the selected POC event/business rule.
- [ ] Full inventory/procurement scope has not been accidentally introduced.

---

# 9. Charge / Finance Boundary

Apply whenever ChargeItem, billing or finance views change.

- [ ] ChargeItem originates from the supported clinical/business event.
- [ ] Charge references the correct tenant/patient/encounter where required.
- [ ] Finance can access required charge/billing information.
- [ ] Finance cannot access prohibited clinical content.
- [ ] Mixed-role behavior preserves the clinical denial rule defined by the project contract.
- [ ] Clinical note/result bodies are not copied into finance tables merely for convenience.
- [ ] POC does not claim production claims/eClaim support.

Critical question:

Can `R-FIN` obtain SOAP notes, detailed clinical results or other
prohibited clinical content through this change?

If yes → FAIL unless explicitly authorized by the governing source.

---

# 10. Authorization

Apply to every protected route or protected operation.

- [ ] Authorization is deny-by-default.
- [ ] Positive permission case is tested.
- [ ] Negative permission case is tested.
- [ ] Role checks occur server-side.
- [ ] UI visibility is not treated as authorization.
- [ ] Tenant isolation cannot be bypassed by changing an ID.
- [ ] Finance/Admin clinical restrictions are preserved.
- [ ] Authorization failure does not leak protected content.

UI role preview is never security evidence.

---

# 11. PHI Access Audit

Apply whenever a protected patient-data read path is added or changed.

- [ ] Protected read produces the required audit evidence.
- [ ] Actor is identifiable.
- [ ] Patient/context is identifiable as required.
- [ ] Timestamp is recorded.
- [ ] Audit failure behavior follows the current contract.
- [ ] Audit record does not unnecessarily duplicate clinical payload.
- [ ] Sensitive request bodies/tokens/DB URLs are not logged.

Passing authorization tests alone is NOT sufficient evidence of audit compliance.

---

# 12. Tenant Isolation

Apply to all patient-domain persistence changes.

- [ ] Tenant identifier exists where required.
- [ ] Database relationships prevent cross-tenant linking where required.
- [ ] Application filtering is not the sole isolation mechanism where the contract requires DB enforcement.
- [ ] Unique constraints have correct tenant scope.
- [ ] Test demonstrates rejection of cross-tenant relationship.
- [ ] Seed data cannot accidentally cross tenants.

Important:

Having a `tenant_id` column alone does NOT prove tenant isolation.

---

# 13. Database / Migration

Apply to every schema change.

- [ ] Versioned Alembic migration exists.
- [ ] Upgrade path is explicit.
- [ ] Downgrade behavior is explicit.
- [ ] No `metadata.create_all()` is used for product startup.
- [ ] Migration was tested against real PostgreSQL when required by the task.
- [ ] Constraints represent domain invariants where appropriate.
- [ ] Migration does not silently destroy clinical history.
- [ ] Seed remains idempotent where required.
- [ ] Migration failure fails closed.

Guardian does not approve a migration merely because SQLite tests pass.

---

# 14. Transaction / Outbox

Apply when a cross-module state transition or event is introduced.

- [ ] Domain write ownership remains clear.
- [ ] Cross-module transition follows the project's transactional outbox contract where applicable.
- [ ] Business state and required outbox event are atomic where required.
- [ ] Retry/idempotency behavior is considered where required.
- [ ] No unnecessary external broker was introduced.
- [ ] No microservice architecture was introduced.

---

# 15. FHIR

Apply only when the task touches the FHIR adapter/export.

- [ ] Supported mapping is explicitly documented.
- [ ] Resource mapping follows the selected FHIR R4 scope.
- [ ] Unsupported FHIR behavior is not claimed.
- [ ] FHIR adapter does not become the internal domain model.
- [ ] Authorization/tenant/audit boundaries still apply.
- [ ] No claim of full FHIR server/conformance is made without evidence.

---

# 16. Synthetic Data / Privacy

Always inspect changed fixtures, seeds and examples.

- [ ] Synthetic data only.
- [ ] No real patient name/data.
- [ ] No real Thai citizen ID.
- [ ] No API key/token/password committed.
- [ ] No production DB URL.
- [ ] No PHI in logs.
- [ ] No PHI in screenshots.
- [ ] No external LLM receives patient data.
- [ ] Demo is clearly distinguishable from clinical production use.

---

# 17. Tests and Evidence

- [ ] Relevant deterministic tests ran.
- [ ] Exit code is available.
- [ ] `SKIP` is not reported as PASS.
- [ ] `NOT_RUN` is not reported as PASS.
- [ ] Tests prove important domain behavior.
- [ ] Negative security tests exist where required.
- [ ] Tenant boundary is tested where relevant.
- [ ] Migration is tested where relevant.
- [ ] Candidate reviewed by Guardian is the same candidate that passed gates.

Tests passing does not automatically mean SRS compliance.

---

# 18. Documentation / Traceability

- [ ] Requirement trace is updated if implementation status changed.
- [ ] Current task acceptance criteria reflect actual behavior.
- [ ] README/docs do not claim unimplemented behavior.
- [ ] Future capabilities remain marked `NOT_IMPLEMENTED`.
- [ ] ADR exists for approved architectural deviation.
- [ ] Evidence corresponds to the reviewed candidate.

---

# 19. Architecture Drift

Check for accidental introduction of:

- [ ] microservices
- [ ] Kafka
- [ ] RabbitMQ
- [ ] Kubernetes
- [ ] external LLM in HIS request path
- [ ] mandatory paid API
- [ ] separate database per module
- [ ] unnecessary distributed architecture
- [ ] real government integration
- [ ] clinical AI/CDS

If introduced without explicit authorization → FAIL.

---

# 20. Final Guardian Verdict

Return exactly one:

## PASS

Use only when:
- applicable checklist items pass;
- deterministic evidence exists;
- no unresolved material SRS/contract conflict exists.

## FAIL

Use when:
- implementation contradicts an applicable authoritative requirement;
- security/domain invariant is violated;
- scope drift occurred.

Each finding must include:

| Field | Required |
|---|---|
| Severity | Yes |
| Source | Yes |
| Affected file | Yes |
| Evidence | Yes |
| Minimal correction | Yes |

## UNCERTAIN

Use when:
- source documents are ambiguous;
- selected excerpts are insufficient;
- requirement cannot be established safely.

State exactly what source or human decision is needed.

Never convert uncertainty into an invented requirement.