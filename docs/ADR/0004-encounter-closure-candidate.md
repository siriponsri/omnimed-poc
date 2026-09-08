# ADR-0004 — Encounter completion prerequisites

Status: PROPOSED / BLOCKED_AMBIGUITY · Findings SG-003/004

BR-CLI-01-03/VR-CLI-01-03 ต้อง signed clinical note และ principal diagnosis ก่อน close; BR-CORE-04 แยก discharged/completed; BR-FIN-02-06/-12 ยังมีประเด็น settlement/receivables. Core demo story ไม่รวม note/diagnosis/accounting implementation จึงไม่อาจนับ ChargeItem ว่า paid หรือ complete

เสนอให้ owner เลือก minimal synthetic note/diagnosis และ settled account path ที่ระบุ proof/status ชัดเจน แล้ว update contract/trace. ไม่รวม debt/receivable, real receipt หรือ Next Account posting. จนกว่าจะยอมรับ decision M5-03 ไม่เปิด complete endpoint. M1 planned/in_progress และ M2/M3 worklists ทำต่อได้โดยไม่ bypass closure
