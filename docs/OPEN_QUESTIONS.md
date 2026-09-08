# Findings and decisions before clinical tasks

คำถามเหล่านี้ไม่ขัดขวางการสร้าง M0 source แต่ต้องปิดก่อน task ที่ระบุ. เก็บ source snapshot เดิมและลง disposition ที่นี่; ไม่ rewrite SRS

| Finding | Evidence / issue | Disposition | Gate / owner |
|---|---|---|---|
| SG-001 | ต้นฉบับอ้าง ADR-001/002, Next Account architecture/schema/plan และ ai-agent-routing | Course พบและอ่านแล้ว; historical ADR/Next Account files ยังไม่มี. ไม่อนุมานเนื้อหา; ไม่ block M0 | Owner จัดหาเมื่อเริ่ม dependency; ดู source/RECONCILIATION |
| SG-002 | BR-CORE-12 ให้ revoke predecessor แต่ห้าม UPDATE ทุกกรณี | PROPOSED ADR-0002: immutable clinical payload + permitted lifecycle state changes + append-only history. ยังไม่ยอมรับแทน SRS เงียบ ๆ | BLOCKED M3-00/M3-02; domain owner |
| SG-003 | BR-CLI-01-03 / VR-CLI-01-03 ต้อง principal diagnosis + signed note; demo story ไม่กล่าวถึง | ยังไม่ implement completion. ขอ freeze minimum synthetic note/diagnosis scope ก่อน M5-03; ห้าม charge=complete | BLOCKED M5-00; domain owner |
| SG-004 | BR-FIN-02-06 vs BR-FIN-02-12: settled account กับ nonpayment/receivables close | เสนอเฉพาะ synthetic settled path; debt/receivable path ยัง excluded. ต้องกำหนดสถานะและหลักฐาน settlement; ไม่สร้าง payment/receipt ปลอม | BLOCKED M5-00/M5-03; domain owner |
| SG-006 | A05 ใช้ R-LAB ขณะที่ SRS แยก R-LAB-SUP | Master อนุญาต 7 roles; planned tenant config อนุญาต demo single operator ตาม US-ANC01-05. ต้อง explicit permission, section filter และ negative tests | Accepted POC reduction; M4-00/M4-02 |
| SG-005 | Mockup lab charge ตอน release ขัด BR-ANC01-11 technical_complete | SRS wins: charge via order.fulfilled at technical_complete; result.released ไม่ charge | Resolved precedence; M4-01/M4-04 |
| SG-008 | CPOE SRS มี CDS และ pharmacy/finance มี real stock | Master/HANDOFF explicitly exclude; disable CDS claims, synthetic catalog inventory_item_id=null; ไม่แกล้ง decrement stock | Authorized reduction; M3/M4 |
| SG-B01 | Full-check เดิมตรวจ config แต่ไม่ start Compose | แก้ด้วย scripts/compose_smoke.py แยก disposable project, actual HTTP/Postgres/browser/outage gates | Source fix complete; runtime verification M0-01 ยัง NOT_RUN |
| ENV-001 | Work runtime ไม่มี Docker daemon/live PostgreSQL | Full local runtime/migration ไม่ได้รัน. มี executable gate และ GitHub CI; ไม่ให้ release PASS จาก unit tests | BLOCKED_ENVIRONMENT M0-01 |
| DEP-001 | Railway เพิ่มจาก user instruction หลัง freeze | D01 / ADR-0005 อนุญาต GitHub demo configuration; local topology คงเดิม; ใช้ current IaC + UI steps | Implemented config; actual cloud NOT_RUN |

SG-007: production RLS/encryption deferred โดย master; SG-009: adult self-relation + generated HN ไม่เลือก full guardian flow; SG-010: exact SRS IDs/locators ไม่ใช้ mockup aliases; SG-011: ไม่คัดลอก fake KPI/placeholder TMT/dose advice; SG-012: R-ADM ต่างจาก R-ADMIN และ support-role deny wins. รายละเอียด/severity อยู่ docs/source/findings.json; ทุก finding คง source identity เดิม

## รูปแบบคำตอบที่ต้องการเมื่อถึง task

M3: อนุญาตให้แก้เฉพาะ lifecycle status ของ predecessor พร้อม immutable payload/history หรือจะเลือก representation อื่นที่ยัง revoke ได้อย่างไร? ระบุ actor/reason/concurrency behavior และเพิ่ม acceptance examples

M5: ยอมรับ scope เพิ่ม minimal signed synthetic note + principal diagnosis สำหรับ completion หรือคง endpoint completion ปิดไว้? กำหนด allowed code/version หากต้องใช้รหัสจริง. ระบุ account settlement ที่จำลองได้โดยไม่อ้างว่าเชื่อมบัญชีจริง. การเลือกต้องลง ADR/contract/trace และ tests ก่อน code

ไม่ต้องตัดสินใจเรื่องนี้เพื่อเปิด M0 shell. ห้ามใช้ intuition เติม regulatory versions, clinical reference ranges, live drug codes หรือ accounting semantics
