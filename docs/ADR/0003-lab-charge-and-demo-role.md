# ADR-0003 — Lab event timing and demo operator

Status: ACCEPTED precedence / POC reduction; implementation pending · Sources: BR-ANC01-11, US-ANC01-05, master A05

Lab charge เกิดเมื่อ analysis technical_complete ตาม SRS ไม่ใช่ตอน result release ที่ mockup แสดง. Future mapping ใช้ order.fulfilled เป็น reference event ที่ชี้ performed analysis; result.released สร้าง released Observation และไม่สร้าง charge ซ้ำ

รักษา sample → sample_item → analysis → result provenance. Hb 10.2 g/dL เป็นค่าตัวอย่างสังเคราะห์ ไม่มีการวินิจฉัยหรือ reference range ที่อนุมานเอง. UI ต้องเรียก panel ว่า CBC demo (Hb only) หากมีแค่ Hb

Master จำกัด demo 7 roles และให้ R-LAB validate. POC ใช้ explicit tenant configuration สำหรับ single operator; ไม่เพิ่ม production supervisor equivalence. M4-00 freeze permission/section rules และ M4-02 ตรวจ deny เมื่อ flag ปิดหรืออยู่นอก section. ไม่มี lab/result/charge implementation ใน M0
