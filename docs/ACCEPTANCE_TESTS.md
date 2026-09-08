# Acceptance specifications

A01–A10 เป็น **NOT_IMPLEMENTED / NOT_RUN** สำหรับ clinical features ใน v0.1. ข้อความ Given/When/Then เป็น test contract ของ milestones ถัดไป ไม่ใช่ผลทดสอบ. ทุก scenario ใช้ synthetic tenant, adult patient และ actor ที่ authenticated แล้ว; user-supplied role header ไม่ให้อำนาจ

| ID | Given | When | Then / negative case | Milestone |
|---|---|---|---|---|
| A01 | ยังไม่มี Somchai Demo และ R-REG มีสิทธิ์ | ค้นหาก่อนลงทะเบียน synthetic patient | Party + Patient + self relation + generated HN/identifier ถูกสร้าง atomically; search พบ; concurrent HN ไม่ซ้ำ, invalid DOB ถูกปฏิเสธ, anonymous denied | M1 |
| A02 | Patient มีอยู่ใน tenant เดียวกัน | R-REG เปิด OPD visit | Encounter class AMB/status planned ผูก Patient; doctor first-call เปลี่ยน in_progress พร้อม history; cross-tenant link denied | M1/M2 |
| A03 | Encounter อยู่ในสถานะที่ triage อนุญาต | R-SCR บันทึก BP/temperature/weight | มี ObservationDefinition/Observation, BP parent/children, unit/effective time/ref snapshot; ไม่มี weight_kg/temp บน Encounter; invalid/unit mismatch ไม่บันทึก | M2 |
| A04 | Doctor เปิด encounter และ catalog active | สั่ง CBC demo (Hb only) | Encounter-linked Order เข้า assigned lab worklist; ยังไม่เกิด charge; invalid actor/catalog denied | M3/M4 |
| A05 | มี sample → sample_item → analysis/result ของ lab order | Authorized R-LAB กรอก synthetic Hb 10.2 g/dL แล้ว validate/release ภายใต้ demo permission | Released result สร้าง Observation พร้อม provenance/ref snapshot; Doctor อ่านได้; unreleased result ไม่เปิดเผย; correction link ประวัติเดิม ไม่ overwrite | M4 |
| A06 | Doctor มีสิทธิ์และ encounter ถูกต้อง | สั่ง synthetic Paracetamol 500 mg พร้อม structured detail | Medication type ของ Order เดียวกันเข้า pharmacy worklist; quantity/dose/route validation ทำงาน; ไม่อ้าง CDS หรือคำแนะนำรักษา | M3/M4 |
| A07 | Active unrevoked medication order | R-PHA จ่ายปริมาณบวกไม่เกิน remaining | Dispense + outbox atomically; consumer สร้าง ChargeItem ด้วย price snapshot; replay ไม่เพิ่ม charge; failed transaction ไม่มี phantom charge | M4 |
| A08 | มี charges จาก lab technical_complete และ dispense | R-FIN เปิด billing | เห็น billing label/quantity/money/identifier เท่าที่จำเป็น; API response/export ไม่มี SOAP, diagnosis, Observation.value หรือ order_detail; R-FIN+R-DOC ยังคงถูก deny clinical read | M4/M5 |
| A09 | Protected patient resource และ local actor | อ่านสำเร็จหรือถูกปฏิเสธ | Audit ระบุ actor/role/action/time/resource/context/outcome โดยไม่คัดลอก clinical payload; export มี audit; app ไม่ให้แก้/ลบ audit | M1 baseline / M5 |
| A10 | Supported synthetic data ผ่าน A01–A07 | Authorized caller ขอ minimal FHIR export | Validate R4 subset Patient/Encounter/Observation/ServiceRequest/MedicationRequest และ references/codes; unsupported search/write คืน error ที่ชัดเจน; finance ถูก deny clinical export | M5 |

Lab charge เกิดที่ `analysis.technical_complete` ตาม BR-ANC01-11 แม้ A05 ยังไม่ release. `result.released` ไม่คิดเงินซ้ำ. Lab validation เป็น planned single-operator demo configuration ไม่ใช่ production supervisor equivalence

## Additional invariant scenarios

- AT-REV: สร้าง revision/discontinue ใหม่, preserve old clinical payload และ chain; concurrent correction ปฏิเสธ stale version; pending ADR-0002 ต้องผ่านก่อน implementation
- AT-CLOSE: clinical discharge ต่างจาก billing completion; unsigned note, absent principal diagnosis, unsettled account ต้องไม่ bypass; SG-003/004 และ ADR-0004 block จน freeze semantics
- AT-DENY: actor, tenant และ section scope ตรวจที่ API/database relationship; invalid object ID ไม่เปิดเผย data ข้าม tenant; hide button อย่างเดียวไม่ผ่าน
- AT-EVENT: domain write/outbox เป็น transaction เดียว; retry consumer ไม่ duplicate charge; failed event handler ยัง retry ได้โดยไม่สูญ reference

## M0 tests ที่มีจริง

| Gate | Existing executable evidence | ขอบเขต |
|---|---|---|
| Backend unit | backend/tests/unit | health sanitized positive/negative probes, fixture determinism, offline migration SQL, env/DSN/PORT |
| PostgreSQL | backend/tests/integration/test_postgresql.py | live up/down/up, model drift, seed twice/conflict, tenant-role/login constraints; opt-in |
| Frontend unit | frontend/tests/readiness.test.ts | allowlist upstream status; secret fields ไม่ถูกส่งต่อ |
| Browser | tests/e2e/foundation.spec.ts | role shell, finance header absence, disabled actions, keyboard/locale/responsive, unavailable status |
| Tooling | tests/tooling | stale/mock evidence and repair budgets cannot create false PASS |
| Full runtime | scripts/compose_smoke.py | built Compose, migration/seed ordering, actual HTTP health, PostgreSQL and browser suite, outage |

ผลการ execute ล่าสุดแยกไว้ใน FINAL_DELIVERY_REPORT; การมี test file ไม่ถือว่ารันผ่านแล้ว
