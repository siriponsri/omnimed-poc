# HANDOFF.md — OmniMed Solo POC → GPT Work

## 1. Purpose

เอกสารนี้เป็น handoff สำหรับให้ GPT Work สร้าง **OmniMed Solo POC Starter** จากเอกสารต้นทางที่ทีมมีอยู่แล้ว

งานรอบนี้ไม่ใช่การสร้าง Hospital Information System ทั้งระบบ และไม่ใช่ production deployment

เป้าหมายคือ:

> สร้าง repository foundation + POC scope contract + implementation plan + multi-agent control plane ที่มีคุณภาพเพียงพอให้ Codex รับช่วง implement OPD vertical slice ต่อได้ทีละ milestone โดยเจ้าของโครงการสามารถเรียนรู้จาก artifact ที่ทำงานจริงภายหลัง

---

## 2. Project Context

OmniMed เป็นแนวคิด Hospital Information System (HIS) แบบ on-premise web application

SRS v2.0 เป็นเอกสาร full-system superset ขนาดใหญ่ ครอบคลุม 53 modules และข้อกำหนดจำนวนมาก ดังนั้นอย่าตีความว่า starter ต้อง implement ทั้งหมด

POC ที่ต้องการคือ **end-to-end OPD clinical/business slice** ไม่ใช่ feature breadth

### Desired POC Journey

```text
Registration
    ↓
Patient
    ↓
OPD Encounter
    ↓
Triage / Vital Signs
    ↓
Doctor / CPOE
    ├───────────────┐
    ↓               ↓
Lab Order      Medication Order
    ↓               ↓
Lab Worklist   Pharmacy Worklist
    ↓               ↓
Lab Result       Dispense
    └───────┬───────┘
            ↓
        ChargeItem
            ↓
          Finance
            ↓
   Encounter Complete
```

---

## 3. Authoritative Inputs

### A. OmniMed SRS v2.0
File:
`OmniMed_SRS_v2.0.docx`

Role:
- authoritative domain semantics
- business rules
- role boundaries
- core data model
- NFR direction
- interoperability direction

Important concepts to preserve:
- Party / Patient separation
- Patient identifiers
- Encounter
- Observation
- Order
- CatalogItem
- ChargeItem
- Role-based access
- Audit
- event/outbox concept
- FHIR R4 orientation

Do not rewrite these concepts casually.

### B. OmniMed UI Mockup v2.0
File:
`OmniMed_UI_Mockup_v2.0.zip`

Role:
- UX / IA reference
- clinical enterprise visual direction
- role/worklist reference
- navigation reference

Not authoritative for business rules when it conflicts with SRS.

### C. AI Agent Routing Course Material
File:
`ai-agent-routing.zip`

Role:
- orchestration concept
- Router → Producer → Checker/Critic → Controller
- adaptive feedback loop
- cost-aware routing
- cross-model verification concept

Use the teaching concept but simplify it into a production-friendly control plane.

---

## 4. Scope Freeze

### POC In Scope

- Registration
- Patient identity minimal subset
- OPD Encounter
- Triage
- Vital Observation
- Doctor workspace
- Lab Order
- Medication Order
- Lab Result
- Pharmacy Dispense
- Charge
- minimal Finance view
- RBAC baseline
- audit baseline
- minimal FHIR R4 mapping/export
- synthetic demo workflow
- local Docker Compose

### Explicitly Out of Scope

- IPD / ICU
- Surgery / OR
- Anesthesia
- Labor / neonatal
- Dental
- Dialysis
- Radiology / DICOM
- Blood Bank
- CSSD
- real stock/procurement
- production claims
- real Thai government integrations
- PACS
- medical devices/analyzers
- LINE/telemedicine
- clinical AI/CDS
- cloud production
- microservices
- Kubernetes

Do not expand scope without user approval.

---

## 5. Architectural Direction

### Preferred shape

```text
Browser
  │
  ▼
Next.js Frontend
  │
  ▼
FastAPI Backend
  │
  ▼
PostgreSQL
  │
  ├── Core clinical/business data
  ├── Audit
  └── Outbox
        │
        ▼
Future adapters
  ├── FHIR
  ├── HL7 v2
  ├── DICOM
  └── Thai external systems
```

Use **modular monolith**.

Do not introduce:
- Kafka
- RabbitMQ
- service mesh
- Kubernetes
- distributed transaction
- separate database per module

unless a future ADR proves it is needed.

---

## 6. Core Data Invariants

### Patient
Patient must not become a dumping ground for guardian/owner relationships.

### Encounter
Represents a care/service encounter and remains central to OPD workflow.

### Observation
Measured values belong here:
- BP
- temperature
- weight
- lab results

Avoid convenience columns that violate the SRS.

### Order
Clinical orders must:
- link to Encounter
- preserve lifecycle/history
- preserve revision relationship

### CatalogItem
One catalog abstraction supports orderable/billable item concepts in the POC subset.

### ChargeItem
Charge should originate from clinical/business events represented by the flow, not arbitrary manual billing in the demo happy path.

### Audit
POC must demonstrate actor/time/context evidence for protected data access implemented in the slice.

---

## 7. User / Role Boundary to Demonstrate

At minimum:

| Role | Can do | Must not expose |
|---|---|---|
| Registration | patient search/register | clinical note |
| Screening Nurse | triage/vitals | finance/admin data beyond need |
| Doctor | clinical view/orders | admin internals |
| Lab | lab worklist/result | unrelated clinical sections |
| Pharmacist | medication worklist/dispense | unnecessary protected detail |
| Finance | charges/billing | SOAP / detailed lab clinical content |
| Admin | configuration/demo admin | clinical chart by default |

RBAC in starter can be POC-grade but documentation must distinguish it from production RLS/IAM requirements.

---

## 8. Multi-Agent Operating Model

Keep only 4 logical agents.

### Orchestrator
Plans and routes tasks.

### Builder
Writes implementation + tests.

### SRS Guardian
Read-only compliance checker.

### Reviewer
Quality/security/maintainability review.

### Required route

```text
Task
 ↓
Builder
 ↓
Deterministic Gates
 ↓
SRS Guardian
 ↓
Reviewer
 ↓
PASS or Findings
```

### Repair budget
- max 2 normal loops
- max 3 difficult loops
- then block for human decision

Never create an autonomous unrestricted agent swarm.

---

## 9. Future Runtime Model Strategy

The owner intends to use:

- Codex for repository implementation
- OpenRouter API later for lower-cost model routing/review
- high-reasoning model only for hard planning/escalation

Therefore:

- no OpenRouter dependency required for product runtime
- no API call required for tests
- no key in repo
- provider abstraction optional
- mock provider required if tooling is scaffolded
- LLM tooling must remain outside the healthcare domain path

---

## 10. External Repositories to Study

These are **references, not dependencies by default**.

### Healthcare

OpenMRS Core  
https://github.com/openmrs/openmrs-core

Bahmni  
https://github.com/bahmni

OpenELIS Global  
https://github.com/openelisglobal

HAPI FHIR  
https://github.com/hapifhir/hapi-fhir

### Coding / Agent

OpenAI Codex  
https://github.com/openai/codex

OpenAI Plugins  
https://github.com/openai/plugins

OpenAI Agents SDK Python  
https://github.com/openai/openai-agents-python

OpenHands Software Agent SDK  
https://github.com/OpenHands/software-agent-sdk

CrewAI  
https://github.com/crewAIInc/crewAI

OpenRouter Examples  
https://github.com/OpenRouterTeam/openrouter-examples

OpenRouter Skills  
https://github.com/OpenRouterTeam/skills

### UI / Writing Quality Skills

Hallmark  
https://github.com/Nutlope/hallmark

No AI Slop  
https://github.com/petergyang/no-ai-slop

### How to use references

For each external repository consulted, record:
- what was inspected
- what design idea was learned
- whether anything was copied
- license
- whether the idea is compatible with OmniMed SRS

Never cargo-cult an external architecture.

---

## 11. Plugin / Skill References

OpenAI plugin examples  
https://github.com/openai/plugins

OpenAI Agents SDK skill example  
https://github.com/openai/plugins/tree/main/plugins/openai-developers/skills/agents-sdk

Codex Plugin Creator skill example  
https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/plugin-creator/SKILL.md

Hallmark skill  
https://github.com/Nutlope/hallmark

No AI Slop skill/plugin  
https://github.com/petergyang/no-ai-slop

OpenRouter skills  
https://github.com/OpenRouterTeam/skills

Skill/plugin usage is optional developer tooling.  
The POC must build/run/test without these tools.

---

## 12. Expected Starter Deliverables

GPT Work should create at least:

- `README.md`
- `AGENTS.md`
- `HANDOFF_TO_CODEX.md`
- `docs/POC_CONTRACT.md`
- `docs/REQUIREMENT_TRACE.md`
- `docs/ARCHITECTURE.md`
- `docs/DOMAIN_MODEL.md`
- `docs/OPD_WORKFLOW.md`
- `docs/ACCEPTANCE_TESTS.md`
- `docs/SECURITY_BOUNDARY.md`
- `docs/FHIR_MAPPING.md`
- `docs/EVENT_MODEL.md`
- `docs/OPEN_QUESTIONS.md`
- `docs/LEARNING_GUIDE.md`
- `.ai/ORCHESTRATOR.md`
- `.ai/BUILDER.md`
- `.ai/SRS_GUARDIAN.md`
- `.ai/REVIEWER.md`
- `.ai/ROUTING_POLICY.md`
- `.ai/TASK_TEMPLATE.md`
- `.ai/FINDING_TEMPLATE.md`
- M0–M5 milestone DAG
- backend/frontend/database starter
- deterministic test gates
- local Docker Compose
- synthetic demo seed approach
- `validation/STARTER_AUDIT.md`
- `validation/FINAL_DELIVERY_REPORT.md`

---

## 13. M0 Only for This GPT Work Run

The starter should be runnable but should **not** secretly implement the whole POC.

Allowed implementation:

- FastAPI health
- Next.js shell
- PostgreSQL connection
- migration infrastructure
- test framework
- lint/typecheck/build
- Docker Compose
- seed framework
- minimal role/navigation shell if useful

Everything else should be planned as M1–M5 tasks.

---

## 14. First Codex Handoff

The first recommended Codex task after GPT Work completes should be something like:

`M1-01: Implement minimal Party/Patient + PatientIdentifier persistence and tests according to POC_CONTRACT.md and REQUIREMENT_TRACE.md.`

Codex should not be asked to “build the whole POC” in one prompt.

---

## 15. Quality Bar

The starter must be:

- understandable by a beginner
- credible to a senior developer
- traceable to the SRS
- runnable offline/local
- deterministic where possible
- honest about unimplemented areas
- free of fake implementation
- free of fake compliance claims
- visually professional
- ready for Codex continuation

---

## 16. Final Rule

If forced to choose between:

A. adding more features  
B. making the starter clearer, safer, tested, and easier to hand off

choose **B**.
