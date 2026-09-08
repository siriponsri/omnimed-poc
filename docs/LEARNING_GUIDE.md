# Learning guide — เรียนจาก artifact

M0 มี code ให้เปิดตามได้; M1–M5 ระบุ planned files/endpoints เพื่อไม่ให้เข้าใจว่ามีแล้ว. อ่าน excerpt เฉพาะ task ก่อนแก้ code

## M0

| สิ่งที่เรียน | อ่าน/สังเกต |
|---|---|
| 1. Feature | เปิดบริการ/ฐานข้อมูลและหน้าจอโครงงาน |
| 2. เหตุผลใน HIS | ตรวจ environment ก่อนแก้ domain |
| 3. Files แรก | backend/app/main.py → database.py → db/migrations/versions/0001_foundation.py → frontend/app/page.tsx |
| 4. Tables | foundation_tenant, foundation_role, foundation_demo_identity |
| 5. API | GET /api/health/live, /api/health/ready, /api/foundation; frontend /api/status |
| 6. UI | Thai/EN role preview, empty worklists, disabled clinical actions |
| 7. Tests | backend/tests/unit, integration/test_postgresql.py, tests/e2e/foundation.spec.ts |
| 8. SRS concepts | NFR-O-01, NFR-U-01, master M0 contract |
| 9. แผน 20 นาที | 5 นาที README; 5 นาที contract; 5 นาที health/migration; 5 นาที validation |
| 10. คำถามให้ Codex | ทำไม live=200 แต่ ready=503 ได้? ชี้ code/test จริง แล้วช่วยปิด M0-01 เมื่อมี Docker |

## M1

| สิ่งที่เรียน | อ่าน/สังเกต |
|---|---|
| 1. Feature | Patient/identifier และ OPD encounter |
| 2. เหตุผลใน HIS | แยกตัวบุคคล อัตลักษณ์และครั้งรับบริการ ไม่ให้ประวัติปะปน |
| 3. Files แรก | tasks/M1-01.md → DOMAIN_MODEL.md → SECURITY_BOUNDARY.md; patients/encounters modules จะสร้างภายหลัง |
| 4. Tables | planned Party, Patient, PartyRelation, PatientIdentifier, Encounter, status history, identity/audit baseline |
| 5. API | planned protected patient search/register และ encounter create/read; ยังไม่มี routes |
| 6. UI | planned registration/search/patient header |
| 7. Tests | planned A01/A02/AT-DENY; concurrent HN และ tenant FK |
| 8. SRS concepts | BR-CORE-01/02, BR-PAT-01-01, BR-PAT-02-03 |
| 9. แผน 20 นาที | 5 นาที Party vs Patient; 5 นาที HN; 5 นาที migration acceptance; 5 นาที auth/audit |
| 10. คำถามให้ Codex | ทำ M1-01 เฉพาะ schema/HN allocator พร้อม PostgreSQL negative tests โดยไม่เปิด patient API |

## M2

| สิ่งที่เรียน | อ่าน/สังเกต |
|---|---|
| 1. Feature | BP/temperature/weight เป็น Observation ส่งให้แพทย์ |
| 2. เหตุผลใน HIS | ค่าที่วัดมีหน่วย เวลา ผู้วัดและประวัติ ไม่ใช่ field เขียนทับบน visit |
| 3. Files แรก | tasks/M2-01.md → source BR-CORE-10/11 → planned observations module |
| 4. Tables | planned ObservationDefinition, Observation parent/child, reference snapshot |
| 5. API | planned protected triage record/read endpoints |
| 6. UI | planned triage form/doctor vitals พร้อม units/time |
| 7. Tests | planned A03; type/unit validation; snapshot preservation; missing≠zero |
| 8. SRS concepts | BR-CORE-10/11, US-PAT-02-02 |
| 9. แผน 20 นาที | 5 นาที Observation; 5 นาที BP panel; 5 นาที snapshot; 5 นาที A03 negatives |
| 10. คำถามให้ Codex | เสนอ schema รักษา BP parent/children และ reference snapshot ตาม SRS ก่อน implement M2-01 |

## M3

| สิ่งที่เรียน | อ่าน/สังเกต |
|---|---|
| 1. Feature | Lab/medication orders และการแก้แบบรักษาประวัติ |
| 2. เหตุผลใน HIS | หน่วยรับคำสั่งต้องรู้ผู้สั่ง เวลา และฉบับที่ active |
| 3. Files แรก | ADR/0002-order-revision-candidate.md → tasks/M3-00.md → EVENT_MODEL.md |
| 4. Tables | planned CatalogItem, Order, lifecycle history, EventOutbox |
| 5. API | planned protected create/revise/discontinue; M0 ยังไม่มี |
| 6. UI | planned CPOE แสดง revision/status ไม่มีคำแนะนำรักษา |
| 7. Tests | planned A04/A06/AT-REV/AT-EVENT และ stale change |
| 8. SRS concepts | BR-CORE-12/13/14/15/16, BR-EVT-01 |
| 9. แผน 20 นาที | 5 นาที SG-002; 5 นาที Order root; 5 นาที outbox; 5 นาที revision tests |
| 10. คำถามให้ Codex | ชี้ ambiguity BR-CORE-12 และเสนอ test cases ของทางเลือก โดยยังไม่แก้ schema |

## M4

| สิ่งที่เรียน | อ่าน/สังเกต |
|---|---|
| 1. Feature | Lab result, dispense และค่าใช้จ่ายจากเหตุการณ์จริง |
| 2. เหตุผลใน HIS | แยกงานที่สั่ง งานที่ทำ ผลที่ปล่อย และยอดเรียกเก็บเพื่อไม่คิดเงินซ้ำ |
| 3. Files แรก | ADR/0003-lab-charge-and-demo-role.md → tasks/M4-01.md → M4-04.md |
| 4. Tables | planned sample/sample_item/analysis/result, Observation, Dispense, ChargeItem, account/outbox |
| 5. API | planned section-scoped lab/result, pharmacy dispense, finance projection |
| 6. UI | planned lab/pharmacy worklists; billing ไม่มี clinical payload |
| 7. Tests | planned A04–A08, replay/rollback, quantity limit, unreleased-result deny |
| 8. SRS concepts | BR-ANC01-11, BR-PHM02-01, BR-CORE-17/18 |
| 9. แผน 20 นาที | 5 นาที provenance; 5 นาที technical_complete vs release; 5 นาที dispense; 5 นาที finance deny |
| 10. คำถามให้ Codex | อธิบาย event sequence ที่ทำให้ release ไม่คิด CBC ซ้ำ พร้อม test โดยไม่แก้ SRS |

## M5

| สิ่งที่เรียน | อ่าน/สังเกต |
|---|---|
| 1. Feature | Trust boundary, FHIR export และ accepted journey |
| 2. เหตุผลใน HIS | ข้อมูลสุขภาพต้องจำกัดผู้อ่าน ตรวจย้อนหลัง และแปลงโดยไม่เปลี่ยนความหมาย |
| 3. Files แรก | SECURITY_BOUNDARY.md → FHIR_MAPPING.md → ADR/0004-encounter-closure-candidate.md |
| 4. Tables | planned AuditEvent/auth; clinical note/diagnosis เมื่ออนุมัติ; ไม่มี FHIR truth store แยก |
| 5. API | planned supported export/accepted completion; unsupported operations explicit |
| 6. UI | planned authenticated role journey; selector ปัจจุบันยังไม่ใช่ login |
| 7. Tests | planned A01–A10, AT-CLOSE/AT-DENY, export validation/audit |
| 8. SRS concepts | BR-ROLE-02, NFR-S-03, BR-PLT-05-01, BR-CLI-01-03 |
| 9. แผน 20 นาที | 5 นาที deny precedence; 5 นาที audit; 5 นาที closure; 5 นาที FHIR |
| 10. คำถามให้ Codex | ตรวจ Finance/FHIR response ว่ามี clinical leak หรือไม่ พร้อม evidence ตาม A08–A10 |
