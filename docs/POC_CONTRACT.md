# OmniMed Solo POC Contract

Contract: POC-v0.1 + deployment amendment D01 · Frozen: 2026-09-08 · Work execution: **M0 only**

เอกสารนี้ freeze ขอบเขตตาม GPT Work Master Prompt §§3, 20 ส่วน M1–M5 เป็นงานของ Codex รอบถัดไป ไม่ใช่ feature ที่ส่งมอบใน v0.1

## C01 — เป้าหมาย

พิสูจน์ OPD journey ใน milestones ถัดไป: Registration → Encounter → Triage → Doctor/CPOE → Lab Order → Lab Result → Medication Order → Pharmacy Dispense → Charge → Encounter Completion.

M0 ต้องรัน FastAPI + Next.js + PostgreSQL ในเครื่องได้ มี health/readiness, reversible migration, deterministic seed ที่ไม่มีผู้ป่วย, test/lint/typecheck/build, Docker Compose และเอกสารส่งต่องาน ไม่สร้าง API ผู้ป่วย คำสั่งยา ผลตรวจ การเงิน หรือ login ปลอม

## C02 — ลำดับอำนาจ

Explicit user/master prompt → SRS v2.0 domain/business rules → contract นี้ → UI mockup → ai-agent-routing → external reference → model intuition. การเปลี่ยน semantic ต้องมี Finding และ ADR; หากการเปลี่ยนกระทบขอบเขตหรือ business rule ที่ไม่ได้รับอนุญาต ให้หยุดเฉพาะงานที่เกี่ยวข้อง

## C03 — Architecture

Modular monolith: Next.js/TypeScript → FastAPI/Pydantic/SQLAlchemy → PostgreSQL ฐานเดียว; Alembic เป็น schema authority. ไม่มี broker, microservices, Kubernetes, paid API หรือ cloud requirement สำหรับ local runtime. Railway เป็น optional demo target ตาม D01. LLM และ OpenRouter อยู่ใน developer tooling เท่านั้นและปิดไว้โดยปริยาย

## C04 — Domain invariants

1. Patient ผูก Party; identifier แยก PatientIdentifier; ไม่เก็บ guardian บน Patient (BR-CORE-01).
2. ค่าที่วัดรวม BP/temperature/weight/Hb อยู่ Observation; reference range เป็น snapshot; ไม่เก็บ measured values บน Encounter (BR-CORE-10/11).
3. Order ผูก Encounter; revision สร้างแถวใหม่ชี้ previous_order_id และเก็บประวัติ (BR-CORE-12/13/14). วิธีจัดการ revoked predecessor กับข้อห้าม UPDATE ยัง BLOCKED_AMBIGUITY ตาม ADR-0002; การแยก lifecycle state ออกจาก immutable payload เป็นข้อเสนอที่ยังต้องยอมรับก่อน M3.
4. ไม่ hard-delete clinical record ใน implemented paths. CatalogItem ที่ใช้แล้วปิด active_to (BR-CORE-16).
5. Finance/administrative roles ไม่อ่าน clinical content (BR-CORE-18, BR-ROLE-01/02). Navigation ไม่ใช่ authorization.
6. ChargeItem เกิดจาก clinical event เช่น analysis.technical_complete (แล็บ; BR-ANC01-11) หรือ dispense; ใช้ billing snapshot ที่ไม่เปิดเผยค่าตรวจ/diagnosis (BR-CORE-17).
7. Adapter แยก FHIR/external semantics ออกจาก domain; เป้าหมาย R4 4.0.1 subset ไม่ใช่ full FHIR server.
8. Business change กับ event_outbox ต้องอยู่ transaction เดียวกันเมื่อเริ่ม implement; consumer ต้อง idempotent (SRS §5).
9. discharged และ completed ต่างกัน; completion ต้องมี explicit billing settlement condition (BR-CORE-04). SRS BR-CLI-01-03 ยังบังคับ principal diagnosis และ signed clinical note; M5 completion task ถูก block จนกว่าจะ freeze minimum note/diagnosis scope อย่างชัดเจน
10. ตารางที่มีข้อมูลผู้ป่วยต้องมี tenant_id, created_at/by, updated_at/by (SRS §4.9). M0 ยังไม่อ้างว่า production RLS/encryption พร้อม

## C05 — Roles และ demo

| Role | ขอบเขตใน POC เป้าหมาย |
|---|---|
| R-REG | ทะเบียน/identifier/เปิดบริการ ไม่มี clinical note |
| R-SCR | triage และ vital observations |
| R-DOC | clinical view, orders, discharge |
| R-LAB | lab worklist, result; validation ตาม C07 |
| R-PHA | medication worklist, dispense |
| R-FIN | billing projection เท่านั้น |
| R-ADMIN | demo/master configuration ไม่มี clinical chart โดยปริยาย |

M0 มี role navigation preview และ seed identity fixtures เท่านั้น ไม่มี authenticated demo accounts. การเลือก role เป็นการสำรวจหน้าจอ ไม่ให้สิทธิ์เข้าถึง API

Core story สำหรับ M1–M5: Somchai Demo, system-generated HN, AMB encounter, BP/temperature/weight, CBC/Hemoglobin, synthetic Hb 10.2 g/dL, Paracetamol 500 mg, charge CBC + ยาที่จ่าย. ไม่มี citizen ID จริง ไม่มีคำแนะนำรักษาหรือ clinical AI. M0 ไม่มี patient rows และไม่แสดงจำนวนผู้ป่วยปลอม

## C06 — Exclusions

ห้าม implement IPD, ICU, OR, anesthesia, labor/neonatal, dental, hemodialysis, radiology/DICOM, blood bank, CSSD, PACS, analyzers/devices, real stock/procurement, 43-file, eClaim, NHSO/SSO/CSMBS, MOPH Refer, LINE OA, telemedicine, mobile production app, clinical AI/CDS/diagnosis assistance, production DR/HA, production key lifecycle, production deployment, cloud provisioning นอกขอบเขต D01, microservices หรือ Kubernetes. ไม่สร้าง Next Account ledger; future checkout ใช้ adapter contract เท่านั้น

## C07 — POC reductions และ finding policy

- Single synthetic tenant, human adult demo, no guardian/animal/merge/coverage lifecycle implementation in M0. Domain documents preserve these boundaries.
- Application authorization baseline is deny-by-default when protected routes begin in M1; M0 serves only public non-PHI health/foundation metadata. Clinical RBAC, audit reads and negative tests are required in each introducing task, not postponed until M5.
- RLS, field encryption, real IAM, key rotation and legal compliance remain deferred, explicitly permitted by master §§5/13.
- Master A05 gives result validation to R-LAB while SRS roles distinguish R-LAB-SUP. Record POC-only explicit-user exception in ADR/finding; no production equivalence. M4 must make validation permission explicit and test section scope; do not silently merge source roles.
- CBC and medication prices use labelled synthetic fixtures. No clinical reference ranges or drug prescribing defaults inferred from the demo numbers.
- Encounter closure on unsettled debt is ambiguous in SRS; ordinary settled demo path can be planned, but debt/receivable closure is excluded pending domain decision.
- M0 provides FHIR mapping documents only. No adapter returns fabricated resources; minimal validated export is M5 work.
- Installation needs downloaded packages/images once; normal local runtime and tests make no LLM or external service requests. Offline operation means after provisioning dependencies.

## C08 — Acceptance and release

A01–A10 are specifications, not passed tests in this release. M0 gates verify source tree, no secrets/PHI, health live/ready (including database failure), PostgreSQL migration up/down/up, idempotent seed, role shell, lint/typecheck/build, Compose configuration and documented commands. Every execution claim must cite a retained command/result. Unsupported environment gates stay NOT_RUN and must not be represented as PASS.

## C09 — Change control

Change contract version and trace with an ADR for architecture/invariant changes. Max two normal repair loops, three for hard blockers; then BLOCKED_REQUIRES_HUMAN. No unlimited swarm or retry. Four logical roles: Orchestrator → Builder → deterministic gates → read-only SRS Guardian → Reviewer → PASS/FIX/BLOCKED.

## Source reconciliation before feature work

SRS Guardian พบ mockup แสดงค่า CBC เกิดตอนปล่อยผล แต่ BR-ANC01-11 ระบุ analysis.technical_complete. เลือก SRS เป็นหลักและไม่ implement charging ใน M0. ข้อเสนอให้ revoked ของ order ต้นทางเป็น lifecycle transition พร้อม history และ immutable clinical payload ยังรอ ADR-0002; ไม่ถือเป็น approved SRS interpretation ใน M0. Encounter เริ่ม planned ตาม PAT-02 แล้ว in_progress เมื่อแพทย์เรียก; M1 ต้อง preserve ข้อนี้. ดู OPEN_QUESTIONS และ ADR ก่อนทำ task ที่เกี่ยวข้อง

## D01 — Deployment amendment จาก explicit user instruction

Docker Compose เป็น authoritative local/on-premise topology และต้องผ่าน runtime gate ก่อน release PASS. เพิ่ม Railway demo ที่ deploy จาก GitHub ได้โดยใช้ Dockerfiles เดิม: frontend, backend และ PostgreSQL ฐานเดียว ไม่แยก domain เป็น microservices. อนุญาต config, environment documentation, health check, migration/start/seed commands และคู่มือ `DEMO_DEPLOYMENT.md`; ยังไม่ได้สั่งให้สร้าง cloud resource หรือ publish จริง

Railway ใช้ dedicated environment ชื่อ `demo`, `APP_ENV=demo` และต้องยืนยัน `SYNTHETIC_DEMO_ONLY=true`. Flag นี้เป็น acknowledgement ไม่ใช่ตัวตรวจจับ PHI. M0 ไม่มี clinical input/API และ seed มีเฉพาะ synthetic tenant/role/non-login identities. ห้ามนำ database backup, secrets หรือข้อมูลผู้ป่วยจริงขึ้น demo. มี public domain เฉพาะ frontend; backend/database ใช้ private network. Local ไม่ต้องใช้ Railway account, SDK, token หรืออินเทอร์เน็ตเมื่อเตรียม dependencies แล้ว

การตรวจ config/SDK typecheck ไม่เท่ากับ cloud deployment ผ่าน. ต้องบันทึก actual deployment verification แยกจาก local gates. SRS NFR-O-01 ยังยึด Compose; D01 ไม่เปลี่ยน clinical semantics หรือขยาย M0 เป็น clinical demo
