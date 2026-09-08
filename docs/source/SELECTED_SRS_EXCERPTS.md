# Selected OmniMed SRS excerpts

Quoted text was extracted from the provided DOCX without translating or normalizing requirement IDs. Table cells are shown separately; source locators are B#### plus a 1-based table row where applicable. Excerpts remain authoritative source text, not proof of implementation.

Source file SHA-256: `b9e96f75e642c6a2f06016e1b90a78e8cbcb1d51c93a0ac996a8b83f733724d7`

## NFR-O-01

Source: B0268, table row 2. Planned milestone: M0. Trace status: PARTIAL_POC.

> NFR-O-01
> ติดตั้งด้วย Docker Compose ชุดเดียว ตั้งค่าผ่านไฟล์เดียว

## NFR-O-02

Source: B0268, table row 3. Planned milestone: M0. Trace status: PARTIAL_POC.

> NFR-O-02
> ต้องมี endpoint สำหรับตรวจสุขภาพระบบ (/health, /ready) และ metrics

## NFR-O-04

Source: B0268, table row 5. Planned milestone: M0. Trace status: PARTIAL_POC.

> NFR-O-04
> การอัปเกรดเวอร์ชันต้องมี migration script ที่ย้อนกลับได้ และต้องไม่ทำให้ข้อมูลเดิมอ่านไม่ได้

## BR-PLT-07-10

Source: B3198, table row 11. Planned milestone: M0. Trace status: PARTIAL_POC.

> BR-PLT-07-10
> migration ต้องย้อนกลับได้และต้องไม่ทำให้ข้อมูลเดิมอ่านไม่ได้ (NFR-O-04) — การอัปเกรดที่มี migration ทำลายข้อมูลต้องถูกปฏิเสธที่ขั้น preflight

## VR-PLT-07-07

Source: B3202, table row 8. Planned milestone: M0. Trace status: PARTIAL_POC.

> VR-PLT-07-07
> preflight ของ migration ต้องผ่านทุกข้อจึงจะเริ่มได้ ผลลัพธ์ต้องถูกบันทึก

## NFR-U-01

Source: B0264, table row 2. Planned milestone: M0. Trace status: PARTIAL_POC.

> NFR-U-01
> ภาษาหลักไทย รองรับอังกฤษเต็มรูปแบบ สลับได้รายผู้ใช้

## NFR-U-04

Source: B0264, table row 5. Planned milestone: M0. Trace status: PARTIAL_POC.

> NFR-U-04
> หน้าจอที่ใช้ในพื้นที่ให้บริการต้องทำงานได้บนหน้าจอ 1366×768 ขึ้นไป และรองรับการใช้แป้นพิมพ์ล้วน

## BR-PLT-07-01

Source: B3198, table row 2. Planned milestone: M0/M1. Trace status: PARTIAL_POC.

> BR-PLT-07-01
> ทุกตารางที่มีข้อมูลผู้ป่วยต้องมี tenant_id และ session ต้องถูกผูก tenant_id เสมอ — ไม่มีทางอ่านข้ามผู้เช่า แม้ในระดับผู้ดูแลระบบ (ข้อ 4.9)

## BR-PLT-07-05

Source: B3198, table row 6. Planned milestone: M0/M1. Trace status: PARTIAL_POC.

> BR-PLT-07-05
> เวลาทั้งหมดจัดเก็บเป็น UTC และแปลงตามเขตเวลาของผู้เช่าเมื่อแสดง — ปีพุทธศักราชเป็นเรื่องของชั้นการแสดงผลเท่านั้น ห้ามเก็บ พ.ศ. ลงฐานข้อมูล

## VR-PLT-07-01

Source: B3202, table row 2. Planned milestone: M0/M1. Trace status: PARTIAL_POC.

> VR-PLT-07-01
> tenant_id ต้องไม่ว่างในทุกแถวของตารางที่มีข้อมูลผู้ป่วย — บังคับด้วย NOT NULL และนโยบาย RLS

## VR-PLT-07-08

Source: B3202, table row 9. Planned milestone: M0/M1. Trace status: PARTIAL_POC.

> VR-PLT-07-08
> เขตเวลาของผู้เช่าต้องเป็นค่าจากฐานข้อมูล IANA ที่ถูกต้อง

## BR-EVT-01

Source: B0238. Planned milestone: M0/M3/M4. Trace status: PARTIAL_POC.

> BR-EVT-01 event ต้อง immutable และมี event_id แบบ UUID เพื่อให้ผู้บริโภคทำ idempotency ได้

## BR-EVT-02

Source: B0238. Planned milestone: M0/M3/M4. Trace status: PARTIAL_POC.

> BR-EVT-02 ผู้บริโภคต้องรองรับการได้รับ event ซ้ำ

## BR-EVT-03

Source: B0238. Planned milestone: M0/M3/M4. Trace status: PARTIAL_POC.

> BR-EVT-03 ห้ามใส่ข้อมูลเวชระเบียนเต็มรูปแบบใน payload — ใส่เฉพาะ reference id ให้ผู้บริโภคที่มีสิทธิ์ไปอ่านเอง

## BR-PLT-07-06

Source: B3198, table row 7. Planned milestone: M0/M3/M4. Trace status: PARTIAL_POC.

> BR-PLT-07-06
> event ต้องเขียนลง event_outbox ในธุรกรรมเดียวกับการเปลี่ยนข้อมูล ห้ามใช้ distributed transaction (ข้อ 5)

## VR-PLT-07-05

Source: B3202, table row 6. Planned milestone: M0/M3/M4. Trace status: PARTIAL_POC.

> VR-PLT-07-05
> รายการใน event_outbox ต้องมี event_id UUID ที่ไม่ซ้ำ และมี occurred_at

## BR-EVT-04

Source: B0238. Planned milestone: M0. Trace status: DEFERRED.

> BR-EVT-04 ต้องมีหน้าจอสำหรับผู้ดูแลระบบเพื่อดูสถานะ event ที่ค้างและสั่ง replay ได้

## BR-PLT-07-07

Source: B3198, table row 8. Planned milestone: M0. Trace status: DEFERRED.

> BR-PLT-07-07
> ต้องมีหน้าจอดู event ค้างและสั่ง replay ได้ (BR-EVT-04) และการ replay ต้องปลอดภัยเพราะ event มี event_id UUID และผู้บริโภคทำ idempotency (BR-EVT-01, BR-EVT-02)

## BR-PLT-07-08

Source: B3198, table row 9. Planned milestone: M0. Trace status: DEFERRED.

> BR-PLT-07-08
> event ที่ล้มเหลวเกินจำนวนครั้งที่กำหนดต้องเข้าคิว dead letter ไม่ใช่ถูกทิ้ง และต้องแจ้งเตือนผู้ดูแล

## BR-CORE-01

Source: B0147. Planned milestone: M1. Trace status: SELECTED.

> BR-CORE-01 ห้ามเก็บชื่อผู้ปกครองเป็นคอลัมน์ใน patient — ต้องผ่าน party_relation เสมอ

## BR-PAT-01-03

Source: B0309, table row 4. Planned milestone: M1. Trace status: SELECTED.

> BR-PAT-01-03
> ห้ามเก็บชื่อผู้ปกครองหรือเจ้าของเป็นคอลัมน์ใน patient ต้องผ่าน party_relation เสมอ (BR-CORE-01)

## BR-PAT-01-01

Source: B0309, table row 2. Planned milestone: M1. Trace status: PARTIAL_POC.

> BR-PAT-01-01
> HN ต้องไม่ซ้ำภายใน tenant_id และเมื่อออกแล้วห้ามนำกลับมาใช้ใหม่แม้ระเบียนจะถูก merge

## BR-PAT-01-02

Source: B0309, table row 3. Planned milestone: M1. Trace status: PARTIAL_POC.

> BR-PAT-01-02
> รูปแบบ HN ตั้งค่าได้ระดับผู้เช่า (prefix + ปี พ.ศ./ค.ศ. + running) และการเปลี่ยนรูปแบบต้องไม่กระทบ HN ที่ออกไปแล้ว

## BR-PAT-01-04

Source: B0309, table row 5. Planned milestone: M1. Trace status: PARTIAL_POC.

> BR-PAT-01-04
> ผู้ป่วยหนึ่งรายมี patient_identifier ที่ is_preferred = true ได้เพียงหนึ่งรายการต่อ identifier_type

## VR-PAT-01-02

Source: B0313, table row 3. Planned milestone: M1. Trace status: PARTIAL_POC.

> VR-PAT-01-02
> วันเกิดต้องไม่อยู่ในอนาคต และอายุที่คำนวณได้ต้องไม่เกิน 130 ปี — เกินให้เตือนแต่บันทึกได้พร้อมเหตุผล

## VR-PAT-01-03

Source: B0313, table row 4. Planned milestone: M1. Trace status: PARTIAL_POC.

> VR-PAT-01-03
> ต้องมี identifier อย่างน้อยหนึ่งรายการเสมอ (HN นับเป็นหนึ่ง)

## US-PAT-01-01

Source: B0301, table row 2. Planned milestone: M1. Trace status: PARTIAL_POC.

> US-PAT-01-01
> ในฐานะ R-REG ฉันต้องการค้นหาผู้ป่วยจากข้อมูลบางส่วน (HN, เลข 13 หลัก, ชื่อ, นามสกุล, วันเกิด, เบอร์โทร) เพื่อไม่สร้างระเบียนซ้ำ
> ค้นด้วยคำค้นเดียวข้ามหลายฟิลด์ได้ · รองรับชื่อไทยแบบไม่คำนึงวรรณยุกต์และสระที่พิมพ์ต่างกัน · คืนผลภายใน 1 วินาทีที่ 500,000 ระเบียน (NFR-P-01) · แสดงคะแนนความคล้าย และเตือนเมื่อพบระเบียนคล้ายกัน ≥ เกณฑ์

## SC-PAT-01-01

Source: B0305, table row 2. Planned milestone: M1. Trace status: PARTIAL_POC.

> SC-PAT-01-01
> ค้นหาผู้ป่วย
> ช่องค้นเดียว + ตัวกรองขั้นสูง · ตารางผล (HN, ชื่อ, อายุ, เพศ, สิทธิ์ปัจจุบัน, visit ล่าสุด) · ปุ่ม “ลงทะเบียนใหม่” ที่ปิดอยู่จนกว่าจะค้นแล้วอย่างน้อยหนึ่งครั้ง · รองรับแป้นพิมพ์ล้วน (NFR-U-04)

## SC-PAT-01-02

Source: B0305, table row 3. Planned milestone: M1. Trace status: PARTIAL_POC.

> SC-PAT-01-02
> ลงทะเบียนผู้ป่วยใหม่
> ปุ่ม “อ่านบัตรประชาชน” · ฟอร์มข้อมูล party + patient · ส่วนความสัมพันธ์ (ผู้ปกครอง/เจ้าของ/ผู้ชำระเงิน/ผู้ติดต่อฉุกเฉิน) · ส่วนสิทธิ์เบื้องต้น (เรียก PAT-04) · แถบเตือน “พบระเบียนคล้ายกัน n รายการ” แบบ real-time

## SC-PAT-01-03

Source: B0305, table row 4. Planned milestone: M1. Trace status: PARTIAL_POC.

> SC-PAT-01-03
> แฟ้มข้อมูลผู้ป่วย (Patient Header + Demographics)
> แถบหัวคงที่ (HN, ชื่อ, อายุ, เพศ, แพ้ยา, สิทธิ์, ธงพิเศษ) ที่ปรากฏในทุกโมดูลคลินิก · แท็บ: ข้อมูลส่วนตัว, ตัวตน/เลขประจำตัว, ความสัมพันธ์, สิทธิ์, ประวัติการมารับบริการ, เอกสารแนบ, ประวัติการแก้ไข

## BR-CORE-02

Source: B0147. Planned milestone: M1. Trace status: SELECTED.

> BR-CORE-02 การรวมระเบียนซ้ำเป็นการทำเครื่องหมาย ไม่ใช่การลบ ระเบียนที่ถูกรวมต้องยังอ่านได้และชี้ไปยังระเบียนหลัก

## NFR-Q-02

Source: B0260, table row 3. Planned milestone: M1. Trace status: SELECTED.

> NFR-Q-02
> ห้ามลบระเบียนทางคลินิกอย่างถาวร — ใช้ entered_in_error แทน และยังต้องอ่านย้อนหลังได้

## BR-PAT-02-01

Source: B0358, table row 2. Planned milestone: M1/M2. Trace status: PARTIAL_POC.

> BR-PAT-02-01
> การออกคิวสร้าง encounter ที่ encounter_class = AMB และ status = planned — จะเป็น in_progress เมื่อถูกเรียกเข้าห้องตรวจครั้งแรก

## BR-PAT-02-02

Source: B0358, table row 3. Planned milestone: M1/M2. Trace status: PARTIAL_POC.

> BR-PAT-02-02
> ผู้ป่วยหนึ่งรายมี encounter ที่ status = in_progress ในวันเดียวกันได้มากกว่าหนึ่งรายการเฉพาะเมื่อ service_type ต่างกัน — มิฉะนั้นต้องเตือนซ้ำซ้อน

## BR-PAT-02-03

Source: B0358, table row 4. Planned milestone: M1/M2. Trace status: PARTIAL_POC.

> BR-PAT-02-03
> คิวเป็นสิ่งชั่วคราวที่อ้าง encounter ห้ามเก็บข้อมูลคลินิกไว้ในตารางคิว

## US-PAT-02-01

Source: B0350, table row 2. Planned milestone: M1/M2. Trace status: PARTIAL_POC.

> US-PAT-02-01
> ในฐานะ R-REG ฉันต้องการออกบัตรคิวให้ผู้ป่วยที่มาถึง เพื่อจัดลำดับการรับบริการ
> ออกคิวจากผู้ป่วยที่ระบุตัวตนแล้วหรือจากการนัดหมาย · หมายเลขคิวมี prefix ตามประเภทบริการ · พิมพ์บัตรคิวพร้อมเวลารอโดยประมาณ · ยิง encounter.started

## US-PAT-02-02

Source: B0350, table row 3. Planned milestone: M2. Trace status: PARTIAL_POC.

> US-PAT-02-02
> ในฐานะ R-SCR ฉันต้องการบันทึกสัญญาณชีพและค่าวัดพื้นฐาน เพื่อให้แพทย์เห็นข้อมูลก่อนตรวจ
> บันทึก BT, PR, RR, BP (systolic/diastolic), SpO₂, น้ำหนัก, ส่วนสูง, รอบเอว, pain score · ทุกค่าเขียนลง observation พร้อม LOINC และหน่วย UCUM (BR-CORE-11) · BP เก็บเป็น parent + child (BR-CORE ข้อ 4.4 parent_id) · คำนวณ BMI เป็น observation ที่มี derived_from

## BR-CORE-10

Source: B0172. Planned milestone: M2. Trace status: PARTIAL_POC.

> BR-CORE-10 ค่าอ้างอิงต้อง snapshot ลงในแถว observation ณ เวลาที่ลงผล เพื่อให้ผลย้อนหลังตีความได้ถูกแม้ค่าอ้างอิงเปลี่ยนภายหลัง

## BR-CORE-11

Source: B0172. Planned milestone: M2. Trace status: PARTIAL_POC.

> BR-CORE-11 ห้ามสร้างคอลัมน์เฉพาะโรคใด ๆ ในตารางอื่น (เช่น visit.weight_kg) — ทุกค่าที่วัดได้ต้องอยู่ใน observation

## BR-PAT-02-04

Source: B0358, table row 5. Planned milestone: M2. Trace status: PARTIAL_POC.

> BR-PAT-02-04
> ค่าที่วัดได้ทุกค่าต้องลง observation ห้ามเก็บเป็นคอลัมน์ในตารางคิวหรือ encounter (BR-CORE-11)

## BR-CLI-01-01

Source: B0558, table row 2. Planned milestone: M2. Trace status: PARTIAL_POC.

> BR-CLI-01-01
> ข้อมูลคลินิกทุกชิ้นต้องผูกกับ encounter และ patient — ข้อมูลระดับตลอดชีวิต (แพ้ยา ปัญหาต่อเนื่อง) ผูกกับ patient แต่ต้องบันทึกว่าเกิดขึ้นใน encounter ใด

## BR-CLI-01-02

Source: B0558, table row 3. Planned milestone: M2. Trace status: PARTIAL_POC.

> BR-CLI-01-02
> ค่าที่วัดได้ทุกค่าต้องอยู่ใน observation ห้ามสร้างคอลัมน์เฉพาะโรค (BR-CORE-11) และค่าที่กรอกใน form_data ต้องถูกสกัดออกมาด้วย (BR-CORE-22)

## VR-PAT-02-01

Source: B0362, table row 2. Planned milestone: M2. Trace status: PARTIAL_POC.

> VR-PAT-02-01
> ค่าสัญญาณชีพต้องอยู่ในช่วงที่เป็นไปได้ทางสรีรวิทยา (BT 25–45 °C, PR 20–300 /min, RR 4–80 /min, SBP 40–300 mmHg, SpO₂ 30–100 %) — นอกช่วงห้ามบันทึก

## VR-PAT-02-03

Source: B0362, table row 4. Planned milestone: M2. Trace status: PARTIAL_POC.

> VR-PAT-02-03
> systolic > diastolic เสมอ

## VR-PAT-02-06

Source: B0362, table row 7. Planned milestone: M2. Trace status: PARTIAL_POC.

> VR-PAT-02-06
> effective_at ของ observation ต้องไม่อยู่ในอนาคต และไม่ก่อน encounter.period_start เกินกว่าค่าที่ตั้งไว้

## VR-PLT-02-04

Source: B2957, table row 5. Planned milestone: M2. Trace status: PARTIAL_POC.

> VR-PLT-02-04
> observation_definition ต้องมีหน่วย UCUM ที่ถูกต้องเมื่อชนิดข้อมูลเป็นตัวเลข

## VR-PLT-02-05

Source: B2957, table row 6. Planned milestone: M2. Trace status: PARTIAL_POC.

> VR-PLT-02-05
> ช่วงค่าอ้างอิงต้องไม่ทับซ้อนกันภายในชุดอายุ+เพศเดียวกัน

## BR-PAT-02-10

Source: B0358, table row 11. Planned milestone: M2/M3. Trace status: PARTIAL_POC.

> BR-PAT-02-10
> การคัดกรองต้องบังคับยืนยันสถานะการแพ้ยาก่อนเปลี่ยนสถานะคิวเป็น “รอตรวจ”

## BR-CLI-01-05

Source: B0558, table row 6. Planned milestone: M2/M3. Trace status: PARTIAL_POC.

> BR-CLI-01-05
> ประวัติแพ้ยาต้องมีสถานะเสมอ ค่าว่างไม่ถือเป็น “ไม่แพ้” — ระบบต้องแยก no known allergy ออกจาก unknown เพราะ CDS ตีความต่างกัน

## US-CLI-01-05

Source: B0550, table row 6. Planned milestone: M2/M3. Trace status: PARTIAL_POC.

> US-CLI-01-05
> ในฐานะ R-DOC/R-NUR ฉันต้องการบันทึกประวัติแพ้ยาอย่างมีโครงสร้าง เพื่อให้ระบบเตือนได้จริง
> ระบุสารก่อภูมิแพ้เป็นรหัส (TMT / ATC / substance) ไม่ใช่ข้อความอิสระ · ระบุอาการ ความรุนแรง ความน่าเชื่อถือ (certainty) วันที่เกิด ผู้บันทึก · สถานะ “ไม่ทราบ” และ “ไม่มีการแพ้ที่ทราบ” ต้องเป็นค่าที่บันทึกได้ ไม่ใช่ค่าว่าง

## BR-CORE-15

Source: B0188. Planned milestone: M3. Trace status: SELECTED.

> BR-CORE-15 ทุกสิ่งที่สั่งได้และ/หรือคิดเงินได้ต้องอยู่ในตารางนี้ตารางเดียว — เพราะทุกอย่างจบลงที่ order → charge เหมือนกัน

## BR-CORE-16

Source: B0188. Planned milestone: M3. Trace status: SELECTED.

> BR-CORE-16 ห้ามลบรายการที่เคยถูกสั่ง ให้ตั้ง active_to แทน

## BR-PLT-02-05

Source: B2953, table row 6. Planned milestone: M3. Trace status: SELECTED.

> BR-PLT-02-05
> ห้ามลบข้อมูลหลักที่เคยถูกอ้างอิงในธุรกรรม — ใช้ active_to (BR-CORE-16)

## BR-PLT-02-06

Source: B2953, table row 7. Planned milestone: M3. Trace status: SELECTED.

> BR-PLT-02-06
> รหัส catalog_item ต้องไม่ซ้ำภายใน code_system เดียวกันต่อผู้เช่า และการชนระหว่าง pack ต้องถูกแก้ก่อนติดตั้ง ไม่ใช่เขียนทับเงียบ ๆ

## VR-CLI-02-06

Source: B0612, table row 7. Planned milestone: M3. Trace status: SELECTED.

> VR-CLI-02-06
> รายการที่สั่งต้องมี catalog_item.active_from ≤ วันที่สั่ง < active_to

## BR-CORE-13

Source: B0182. Planned milestone: M3. Trace status: SELECTED.

> BR-CORE-13 ทุกคำสั่งต้องผูกกับ encounter เสมอ

## BR-CLI-02-01

Source: B0608, table row 2. Planned milestone: M3. Trace status: SELECTED.

> BR-CLI-02-01
> ทุกคำสั่งลงตาราง order ตารางเดียว แยกด้วย order_type และรายละเอียดเฉพาะชนิดอยู่ใน order_detail JSONB (BR-CORE-15)

## BR-CLI-02-03

Source: B0608, table row 4. Planned milestone: M3. Trace status: SELECTED.

> BR-CLI-02-03
> คำสั่งต้องผูกกับ encounter เสมอ และผู้สั่งต้องมีสิทธิ์สั่งชนิดนั้น (เช่น R-NUR สั่งยาไม่ได้เว้นแต่เป็น verbal order ที่รอ co-sign)

## BR-PHM01-01

Source: B1755, table row 2. Planned milestone: M3. Trace status: SELECTED.

> BR-PHM01-01
> ทุกคำสั่งยาเป็นแถวใน order ที่ order_type = medication ผูก catalog_item (item_type = drug) และผูก encounter เสมอ ตาม BR-CORE-13

## BR-PHM01-02

Source: B1755, table row 3. Planned milestone: M3. Trace status: SELECTED.

> BR-PHM01-02
> รายละเอียดขนาดยา ความถี่ วิธีให้ ระยะเวลา และเงื่อนไข PRN เก็บใน order.order_detail (JSONB) ตามโครงสร้างที่กำหนดใน JSON Schema — ห้ามสร้างตารางคำสั่งยาแยก

## BR-CORE-12

Source: B0182. Planned milestone: M3. Trace status: BLOCKED_AMBIGUITY.

> BR-CORE-12 การแก้ไขคำสั่งคือการสร้างแถวใหม่ action = REVISE ชี้กลับไปที่ previous_order_id และตั้งแถวเดิมเป็น revoked — ห้าม UPDATE คำสั่งเดิม

## BR-CLI-02-02

Source: B0608, table row 3. Planned milestone: M3. Trace status: BLOCKED_AMBIGUITY.

> BR-CLI-02-02
> ห้าม UPDATE คำสั่งเดิมในทุกกรณี — แก้ไข = REVISE + revoked แถวเดิม (BR-CORE-12)

## BR-CORE-14

Source: B0182. Planned milestone: M3. Trace status: SELECTED.

> BR-CORE-14 การหยุดคำสั่งต่อเนื่อง (เช่น ยาที่ให้ทุกวัน) ใช้ action = DISCONTINUE ไม่ใช่การลบ

## US-CLI-02-04

Source: B0600, table row 5. Planned milestone: M3. Trace status: SELECTED.

> US-CLI-02-04
> ในฐานะ R-DOC ฉันต้องการแก้ไขหรือหยุดคำสั่งที่สั่งไปแล้ว เพื่อปรับตามอาการที่เปลี่ยน
> แก้ไขคือสร้างแถวใหม่ action = REVISE ชี้ previous_order_id และตั้งแถวเดิมเป็น revoked (BR-CORE-12) · หยุดใช้ action = DISCONTINUE (BR-CORE-14) · ผู้รับคำสั่งเดิมได้รับ order.revised / order.discontinued

## US-PHM01-05

Source: B1744. Planned milestone: M3. Trace status: SELECTED.

> US-PHM01-05 ในฐานะแพทย์ ฉันต้องการแก้ไขหรือหยุดคำสั่งยา โดยระบบเก็บสายการเปลี่ยนแปลงไว้ครบ เพื่อให้ตรวจสอบย้อนหลังได้ว่าใครเปลี่ยนอะไรเมื่อไร เกณฑ์การยอมรับ: การแก้ไขสร้างแถวใหม่ action = REVISE ที่ previous_order_id ชี้กลับ และแถวเดิมถูกตั้ง status = revoked — ห้าม UPDATE แถวเดิม (BR-CORE-12); การหยุดใช้ action = DISCONTINUE ไม่ใช่การลบ (BR-CORE-14); หน้าจอต้องแสดง revision chain ทั้งสายพร้อมผู้แก้ เวลา และสิ่งที่เปลี่ยน; หากยาถูกจ่ายไปแล้วบางส่วน การ REVISE ต้องแจ้งเภสัชกรและระบุการจัดการยาที่จ่ายไปแล้ว

## BR-PHM01-03

Source: B1755, table row 4. Planned milestone: M3. Trace status: SELECTED.

> BR-PHM01-03
> การแก้ไขคำสั่งยาต้องเดินตาม BR-CORE-12 (REVISE + previous_order_id + แถวเดิมเป็น revoked) และการหยุดต้องใช้ DISCONTINUE ตาม BR-CORE-14

## US-CLI-02-01

Source: B0600, table row 2. Planned milestone: M3. Trace status: PARTIAL_POC.

> US-CLI-02-01
> ในฐานะ R-DOC ฉันต้องการสั่งยาโดยพิมพ์ชื่อไม่กี่ตัวอักษรแล้วเลือก เพื่อสั่งได้เร็วและถูกต้อง
> ค้นจากชื่อสามัญ ชื่อการค้า และรหัส TMT · แสดงรูปแบบ ความแรง วิธีให้ ราคา และสถานะสต็อก · ตั้งค่า dose/frequency/route/duration แล้วระบบคำนวณจำนวนรวมให้ · สร้าง order ที่ order_type = medication

## US-PHM01-01

Source: B1740. Planned milestone: M3. Trace status: PARTIAL_POC.

> US-PHM01-01 ในฐานะแพทย์ ฉันต้องการสั่งยาโดยพิมพ์ชื่อไม่กี่ตัวอักษรแล้วได้รายการที่ถูกต้อง เพื่อสั่งยาได้เร็วโดยไม่เลือกผิดตัว เกณฑ์การยอมรับ: ค้นได้ทั้งชื่อสามัญ ชื่อการค้า และรหัส; แสดงความแรง รูปแบบ วิธีให้ และสถานะบัญชียา (ในบัญชียาหลักแห่งชาติ / นอกบัญชี / ยาที่ต้องอนุมัติ) ในบรรทัดผลลัพธ์; ยาที่หมดสต็อกหรือถูกระงับต้องแสดงชัดพร้อมทางเลือกทดแทน; รายการที่ active_to ผ่านไปแล้วต้องไม่ปรากฏในผลค้นหา แต่ยังอ่านคำสั่งเก่าได้ ตาม BR-CORE-16

## VR-CLI-02-01

Source: B0612, table row 2. Planned milestone: M3. Trace status: PARTIAL_POC.

> VR-CLI-02-01
> คำสั่งยาต้องมีครบ: catalog_item_id, dose, unit, route, frequency, duration หรือจำนวนรวม — ขาดข้อใดข้อหนึ่งห้ามยืนยัน

## VR-PHM01-01

Source: B1759, table row 2. Planned milestone: M3. Trace status: PARTIAL_POC.

> VR-PHM01-01
> ขนาดยาต้องเป็นตัวเลข > 0 และหน่วยต้องเป็นหน่วยที่ใช้ได้กับรูปแบบยานั้นตาม catalog_item.attributes

## VR-PHM01-03

Source: B1759, table row 4. Planned milestone: M3. Trace status: PARTIAL_POC.

> VR-PHM01-03
> วิธีให้ยา (route) ต้องอยู่ในชุดวิธีที่รูปแบบยานั้นรองรับ (เช่น ยาเม็ดห้ามเลือก IV)

## VR-PHM01-04

Source: B1759, table row 5. Planned milestone: M3. Trace status: PARTIAL_POC.

> VR-PHM01-04
> วันที่เริ่มต้องไม่ก่อนวันเริ่ม encounter และวันสิ้นสุดต้องไม่ก่อนวันเริ่ม

## VR-PHM01-07

Source: B1759, table row 8. Planned milestone: M3. Trace status: PARTIAL_POC.

> VR-PHM01-07
> จำนวนที่สั่งจ่าย (dispense quantity) ต้องสอดคล้องกับขนาด × ความถี่ × จำนวนวัน ภายในเกณฑ์ผ่อนผันที่ตั้งไว้

## US-CLI-02-03

Source: B0600, table row 4. Planned milestone: M3. Trace status: OUT_OF_SCOPE.

> US-CLI-02-03
> ในฐานะ R-DOC ฉันต้องการเห็นการเตือนความปลอดภัยขณะสั่ง ไม่ใช่หลังสั่ง เพื่อป้องกันความผิดพลาด
> CLI-08 ตรวจ ณ เวลาสั่ง: แพ้ยา, ปฏิกิริยาระหว่างยา, ขนาดยาตามน้ำหนัก/อายุ/การทำงานของไต, ยาซ้ำซ้อน, ข้อห้ามตามการวินิจฉัย · การเตือนระดับสูงต้องบังคับให้เลือกเหตุผลก่อนสั่งต่อ · ทุกการข้ามการเตือนถูกบันทึก

## BR-CLI-02-05

Source: B0608, table row 6. Planned milestone: M3. Trace status: OUT_OF_SCOPE.

> BR-CLI-02-05
> คำสั่งที่ถูกบล็อกโดย CDS ระดับสูงสุด (แพ้ยาที่ยืนยันแล้ว) ห้ามข้ามโดยผู้ใช้ทั่วไป — ต้องมีบทบาทที่มีสิทธิ์เฉพาะและบันทึกเหตุผล

## US-PHM01-07

Source: B1746. Planned milestone: M3. Trace status: OUT_OF_SCOPE.

> US-PHM01-07 ในฐานะแพทย์ ฉันต้องการเห็นการแจ้งเตือนความปลอดภัยขณะสั่งยา เพื่อไม่สั่งยาที่ผู้ป่วยแพ้หรือตีกัน เกณฑ์การยอมรับ: ตรวจ ณ เวลาสั่ง — ประวัติแพ้ยาและแพ้ข้ามกลุ่ม, ปฏิกิริยาระหว่างยา, ยาซ้ำซ้อนในกลุ่มเดียวกัน, ข้อห้ามตามภาวะของผู้ป่วย (ตั้งครรภ์ ให้นมบุตร ไตบกพร่อง ตับบกพร่อง), ขนาดเกินช่วงที่กำหนด; การแจ้งเตือนแบ่งระดับความรุนแรง ระดับสูงสุดเป็น hard stop; ทุกการข้ามการแจ้งเตือน (override) ต้องบันทึกเหตุผลและรายงานได้ (กติกาการตรวจของ CLI-08 — PHM-01 เป็นผู้เรียกใช้และแสดงผล)

## BR-CLI-01-03

Source: B0558, table row 4. Planned milestone: M3/M5. Trace status: BLOCKED_AMBIGUITY.

> BR-CLI-01-03
> ปิด encounter ไม่ได้ถ้ายังไม่มี principal diagnosis อย่างน้อยหนึ่งรายการ และไม่มีบันทึกการตรวจที่ลงนามแล้ว

## BR-CLI-01-04

Source: B0558, table row 5. Planned milestone: M3/M5. Trace status: BLOCKED_AMBIGUITY.

> BR-CLI-01-04
> บันทึกที่ลงนามแล้วห้ามแก้ — การแก้ไขต้องเป็น addendum ที่มีเวลาและผู้ทำแยกต่างหาก

## VR-CLI-01-03

Source: B0562, table row 4. Planned milestone: M3/M5. Trace status: BLOCKED_AMBIGUITY.

> VR-CLI-01-03
> encounter หนึ่งรายการมี principal diagnosis ได้เพียงหนึ่งรายการ

## VR-CLI-01-01

Source: B0562, table row 2. Planned milestone: M3/M5. Trace status: BLOCKED_AMBIGUITY.

> VR-CLI-01-01
> รหัสวินิจฉัยต้องมีอยู่ในชุด ICD-10-TM เวอร์ชันที่บังคับใช้ ณ วันที่ให้บริการ (ไม่ใช่เวอร์ชันปัจจุบัน)

## VR-CLI-01-08

Source: B0562, table row 9. Planned milestone: M3/M5. Trace status: BLOCKED_AMBIGUITY.

> VR-CLI-01-08
> ลายมือชื่ออิเล็กทรอนิกส์ต้องผูกกับผู้ใช้ที่ล็อกอินอยู่จริงและมีใบอนุญาตประกอบวิชาชีพที่ยังไม่หมดอายุ

## US-ANC01-03

Source: B0964. Planned milestone: M4. Trace status: PARTIAL_POC.

> US-ANC01-03 — worklist ตาม bench/section ในฐานะนักเทคนิคการแพทย์ประจำหน่วยเคมีคลินิก ฉันต้องการเห็นเฉพาะงานของหน่วยตนเรียงตามความเร่งด่วนและเวลาครบกำหนด เพื่อจัดลำดับงานได้ถูก เกณฑ์การยอมรับ: (ก) worklist กรองตาม test_section ที่ผู้ใช้สังกัด และบังคับที่ชั้น RLS ไม่ใช่ UI (ข) แสดงคอลัมน์ priority (stat ขึ้นก่อนเสมอ) เวลาที่เหลือถึง TAT เป้าหมาย และสถานะ analysis (ค) เลือกหลายรายการเพื่อสร้าง worksheet และส่ง work order ไปเครื่องวิเคราะห์ได้ (ง) รายการที่เกิน TAT เป้าหมายต้องถูกไฮไลต์

## BR-ANC01-01

Source: B0977, table row 2. Planned milestone: M4. Trace status: PARTIAL_POC.

> BR-ANC01-01
> LIS ห้ามสร้าง order ด้วยตนเอง ยกเว้นกรณี reflex ซึ่งต้องสร้างเป็น order ใหม่ action = NEW ผูก encounter เดิม และระบุ reason_code = reflex

## BR-ANC01-02

Source: B0977, table row 3. Planned milestone: M4. Trace status: PARTIAL_POC.

> BR-ANC01-02
> หนึ่ง analysis = หนึ่งรายการตรวจ บนหนึ่ง sample_item เท่านั้น หากรายการเดียวกันต้องทำบนสิ่งส่งตรวจสองชิ้น ให้เป็นสอง analysis

## BR-ANC01-12

Source: B0977, table row 13. Planned milestone: M4. Trace status: PARTIAL_POC.

> BR-ANC01-12
> R-LAB เห็นและแก้ไขได้เฉพาะ analysis ที่อยู่ใน test_section ที่ตนสังกัด บังคับด้วย RLS ตาม BR-ROLE-03

## US-ANC01-04

Source: B0965. Planned milestone: M4. Trace status: PARTIAL_POC.

> US-ANC01-04 — ลงผลด้วยมือพร้อมค่าอ้างอิงตามอายุและเพศ ในฐานะนักเทคนิคการแพทย์ ฉันต้องการให้ระบบแสดงค่าอ้างอิงที่ถูกต้องตามอายุและเพศของผู้ป่วยขณะลงผล เพื่อให้แปลผลได้ถูกทันที เกณฑ์การยอมรับ: (ก) ระบบเลือกช่วงอ้างอิงจาก observation_definition โดยจับคู่ อายุ ณ effective_at และเพศ (ข) ค่าอ้างอิงถูก snapshot ลง observation.ref_low/ref_high ตาม BR-CORE-10 (ค) ระบบคำนวณ interpretation (H/L/N/A/AA) อัตโนมัติแต่ผู้ใช้แก้ไขได้พร้อมเหตุผล (ง) ค่าที่อยู่นอกช่วงวิกฤตต้องขึ้นกล่องเตือนสีแดงและบังคับกรอกช่องทางการแจ้งแพทย์

## US-ANC01-05

Source: B0966. Planned milestone: M4. Trace status: PARTIAL_POC.

> US-ANC01-05 — การรับรองและปล่อยผลโดยหัวหน้า ในฐานะหัวหน้าห้องปฏิบัติการ ฉันต้องการรับรองผลเป็นชุดพร้อมเห็นข้อมูล QC ของรอบนั้น เพื่อไม่ปล่อยผลที่มาจากรอบที่ QC ไม่ผ่าน เกณฑ์การยอมรับ: (ก) หน้าจอ validation แสดงผล ค่าเดิมย้อนหลัง (delta check) และสถานะ QC ของเครื่องในช่วงเวลาเดียวกัน (ข) รายการที่ QC ไม่ผ่านถูกล็อกไม่ให้ปล่อย จนกว่าจะบันทึกการแก้ไขและ override โดย R-LAB-SUP พร้อมเหตุผล (ค) การปล่อยผลสร้าง observation และ publish result.released (ง) ผู้ลงผลกับผู้รับรองต้องเป็นคนละคน เว้นแต่ตั้งค่าอนุญาตไว้ระดับผู้เช่า

## BR-ANC01-05

Source: B0977, table row 6. Planned milestone: M4. Trace status: PARTIAL_POC.

> BR-ANC01-05
> ค่าอ้างอิงต้องถูก snapshot ลง observation ณ เวลาปล่อยผล ตาม BR-CORE-10 — ห้าม join ค่าอ้างอิงตอนแสดงผลย้อนหลัง

## BR-ANC01-06

Source: B0977, table row 7. Planned milestone: M4. Trace status: PARTIAL_POC.

> BR-ANC01-06
> ผลที่ปล่อยแล้วห้ามแก้ไข การแก้ผลคือการสร้าง observation แถวใหม่พร้อม status = corrected และตั้งแถวเดิมเป็น entered_in_error ตาม NFR-Q-02 พร้อม publish result.released ซ้ำโดยระบุว่าเป็นการแก้ไข

## VR-ANC01-03

Source: B0981, table row 4. Planned milestone: M4. Trace status: PARTIAL_POC.

> VR-ANC01-03
> ค่าผลชนิดตัวเลขต้องอยู่ในช่วง absolute_min–absolute_max ของ observation_definition มิฉะนั้นปฏิเสธการบันทึก (ไม่ใช่แค่เตือน)

## VR-ANC01-04

Source: B0981, table row 5. Planned milestone: M4. Trace status: PARTIAL_POC.

> VR-ANC01-04
> หน่วยของผลต้องตรงกับหน่วย UCUM ที่กำหนดใน observation_definition หรือแปลงได้ด้วยตัวคูณที่กำหนดไว้เท่านั้น

## VR-ANC01-07

Source: B0981, table row 8. Planned milestone: M4. Trace status: PARTIAL_POC.

> VR-ANC01-07
> ห้ามส่ง analysis เข้าสถานะ validated หากยังมี result ที่จำเป็น (is_required) ว่างอยู่

## BR-ANC01-11

Source: B0977, table row 12. Planned milestone: M4. Trace status: SELECTED.

> BR-ANC01-11
> charge_item ของรายการตรวจถูกสร้างเมื่อ analysis ถึงสถานะ technical_complete (ทำจริงแล้ว) ไม่ใช่ตอนสั่งหรือตอนรับรอง — รายการที่ถูกปฏิเสธหรือยกเลิกก่อนหน้านั้นต้องไม่คิดเงิน ตาม BR-CORE-17

## US-CLI-02-05

Source: B0600, table row 6. Planned milestone: M4. Trace status: PARTIAL_POC.

> US-CLI-02-05
> ในฐานะ R-DOC ฉันต้องการเห็นผลตรวจที่ออกมาระหว่างที่ผู้ป่วยยังอยู่ เพื่อตัดสินใจต่อได้ทันที
> ผลที่ออกใหม่ขึ้นแจ้งเตือนบนหน้าห้องตรวจ · ค่าวิกฤตขึ้นเป็นการแจ้งเตือนที่ต้องรับทราบ (acknowledge) · เปรียบเทียบกับผลเดิมได้

## US-CLI-01-01

Source: B0550, table row 2. Planned milestone: M4. Trace status: PARTIAL_POC.

> US-CLI-01-01
> ในฐานะ R-DOC ฉันต้องการเห็นภาพรวมผู้ป่วยหน้าเดียวก่อนเริ่มตรวจ เพื่อไม่พลาดข้อมูลสำคัญ
> หน้าเดียวแสดง: ปัญหาที่ยังไม่จบ, แพ้ยา, ยาที่ใช้อยู่, ผลแล็บผิดปกติล่าสุด, สัญญาณชีพครั้งนี้, การมารับบริการ 5 ครั้งล่าสุด, ภูมิคุ้มกัน · เปิดได้ภายใน 2 วินาทีที่ประวัติ 3 ปี (NFR-P-02)

## US-PHM02-01

Source: B1802. Planned milestone: M4. Trace status: PARTIAL_POC.

> US-PHM02-01 ในฐานะเภสัชกร ฉันต้องการคิวห้องยาที่จัดลำดับตามความเร่งด่วนและเวลาที่รอ เพื่อให้ผู้ป่วยได้รับยาตามลำดับที่เป็นธรรมและเคสด่วนไม่ตกค้าง เกณฑ์การยอมรับ: คิวแยกเป็นช่องทาง (OPD ทั่วไป / เร่งด่วน / ยาเย็นและยาควบคุมพิเศษ / IPD unit dose / ยากลับบ้าน); เรียงตาม priority แล้วตามเวลารับใบสั่ง; แสดงเวลารอสะสมของแต่ละใบและเตือนใบที่เกินเป้าหมาย; สถานะแต่ละใบเห็นได้ทั้งจากห้องยาและจากจอเรียกคิว (DIG-04)

## BR-PHM02-01

Source: B1816, table row 2. Planned milestone: M4. Trace status: PARTIAL_POC.

> BR-PHM02-01
> การจ่ายยาต้องอ้าง order ที่ status = active เท่านั้น — คำสั่งที่ revoked หรือ cancelled จ่ายไม่ได้

## BR-PHM02-02

Source: B1816, table row 3. Planned milestone: M4. Trace status: PARTIAL_POC.

> BR-PHM02-02
> หากคำสั่งถูก REVISE หรือ DISCONTINUE ขณะที่ใบจ่ายยังไม่จ่ายออก ระบบต้องหยุดใบนั้นและแจ้งเภสัชกรทันที

## BR-PHM02-03

Source: B1816, table row 4. Planned milestone: M4. Trace status: PARTIAL_POC.

> BR-PHM02-03
> charge_item ของยาถูกสร้างเมื่อเหตุการณ์ medication.dispensed เท่านั้น ตาม BR-CORE-17 และต้องมีชื่อรายการที่พอออกบิลได้โดยไม่เปิดเผยข้อบ่งใช้ ตาม BR-CORE-18

## BR-PHM02-12

Source: B1816, table row 13. Planned milestone: M4. Trace status: PARTIAL_POC.

> BR-PHM02-12
> ผู้จ่ายยาต้องเป็นผู้ที่มีสิทธิ์ R-PHA ที่ยัง active และระบบต้องบันทึกผู้จ่ายจริง ไม่ใช่บัญชีกลางของห้องยา

## VR-PHM02-01

Source: B1820, table row 2. Planned milestone: M4. Trace status: PARTIAL_POC.

> VR-PHM02-01
> จำนวนที่จ่ายต้องเป็นจำนวนเต็มบวก (หรือทศนิยมสำหรับรูปแบบที่แบ่งได้) และต้องไม่เกินจำนวนที่สั่งคงเหลือ

## VR-PHM02-06

Source: B1820, table row 7. Planned milestone: M4. Trace status: PARTIAL_POC.

> VR-PHM02-06
> วันที่จ่ายต้องไม่เป็นวันในอนาคต และต้องอยู่ในช่วงที่ order ยัง active

## BR-PHM02-04

Source: B1816, table row 5. Planned milestone: M4. Trace status: OUT_OF_SCOPE.

> BR-PHM02-04
> การตัดสต็อกเกิดที่ระดับ lot และเกิดพร้อมกับการจ่ายในธุรกรรมเดียวกัน — ห้ามตัดสต็อกล่วงหน้าตอนสั่ง

## VR-PHM02-02

Source: B1820, table row 3. Planned milestone: M4. Trace status: OUT_OF_SCOPE.

> VR-PHM02-02
> lot ที่เลือกจ่ายต้องมียอดคงเหลือเพียงพอ และวันหมดอายุต้องอยู่หลังวันจ่ายตามระยะปลอดภัยที่ตั้งไว้

## BR-FIN-01-11

Source: B2088, table row 12. Planned milestone: M4. Trace status: OUT_OF_SCOPE.

> BR-FIN-01-11
> รายการที่ผูกสต็อกต้องอ้าง lot ที่ตัดจริง — ถ้าตัดสต็อกไม่สำเร็จ charge ต้องค้างสถานะ pending ไม่ใช่ billable

## BR-CORE-17

Source: B0193. Planned milestone: M4. Trace status: SELECTED.

> BR-CORE-17 charge_item ถูกสร้างจาก เหตุการณ์ทางคลินิก เท่านั้น (จ่ายยา ลงผลแล็บ ทำหัตถการ ครองเตียงครบวัน) ไม่ใช่จากการคีย์มือ

## BR-CLI-02-06

Source: B0608, table row 7. Planned milestone: M4. Trace status: SELECTED.

> BR-CLI-02-06
> charge_item เกิดจากเหตุการณ์ทางคลินิก ไม่ใช่จากการสั่ง (BR-CORE-17) — คำสั่งที่ถูกยกเลิกก่อนปฏิบัติต้องไม่ก่อให้เกิดค่าใช้จ่าย

## BR-PHM01-12

Source: B1755, table row 13. Planned milestone: M4. Trace status: SELECTED.

> BR-PHM01-12
> charge_item ของยาเกิดจากเหตุการณ์ จ่ายยา ของ PHM-02 ไม่ใช่จากการสั่ง ตาม BR-CORE-17

## BR-FIN-01-01

Source: B2088, table row 2. Planned milestone: M4. Trace status: SELECTED.

> BR-FIN-01-01
> charge_item ทุกแถวต้องสืบสาวไปยังเหตุการณ์ทางคลินิกได้ — ต้องมี order_id หรือ source_event_id อย่างน้อยหนึ่งอย่าง (ขยายความ BR-CORE-17)

## BR-FIN-01-04

Source: B2088, table row 5. Planned milestone: M4. Trace status: SELECTED.

> BR-FIN-01-04
> ราคาถูก snapshot ลงใน charge_item ณ เวลาเกิดรายการ — การเปลี่ยนผังราคาภายหลังต้องไม่ย้อนไปเปลี่ยนรายการเดิม

## BR-FIN-01-06

Source: B2088, table row 7. Planned milestone: M4. Trace status: SELECTED.

> BR-FIN-01-06
> ห้ามสร้าง charge ให้ encounter ที่ status = cancelled หรือ entered_in_error

## BR-FIN-01-10

Source: B2088, table row 11. Planned milestone: M4. Trace status: SELECTED.

> BR-FIN-01-10
> ทุกครั้งที่สร้าง/ยกเลิก charge ต้องเขียน event_outbox ในธุรกรรมเดียวกัน (BR-EVT-01)

## VR-FIN-01-01

Source: B2092, table row 2. Planned milestone: M4. Trace status: SELECTED.

> VR-FIN-01-01
> quantity > 0 และเป็นจำนวนที่หน่วยของ catalog_item รองรับ (จำนวนเต็มสำหรับเม็ด/ชิ้น, ทศนิยม 2 ตำแหน่งสำหรับ ml/mg)

## VR-FIN-01-04

Source: B2092, table row 5. Planned milestone: M4. Trace status: SELECTED.

> VR-FIN-01-04
> catalog_item.is_billable = true และ occurred_at ต้องอยู่ในช่วง active_from … active_to

## VR-FIN-01-07

Source: B2092, table row 8. Planned milestone: M4. Trace status: SELECTED.

> VR-FIN-01-07
> account_id ต้องอยู่ในสถานะ open เท่านั้นจึงรับ charge ใหม่ได้

## BR-FIN-03-01

Source: B2189, table row 2. Planned milestone: M4. Trace status: PARTIAL_POC.

> BR-FIN-03-01
> ห้ามแก้ไขราคาที่ valid_from ผ่านมาแล้ว — ต้องปิดช่วงเดิมและเปิดช่วงใหม่

## BR-FIN-03-02

Source: B2189, table row 3. Planned milestone: M4. Trace status: PARTIAL_POC.

> BR-FIN-03-02
> ช่วงเวลาของ charge_item_definition ที่มีคีย์จำเพาะเดียวกัน ต้องไม่ทับซ้อนกัน

## BR-FIN-03-05

Source: B2189, table row 6. Planned milestone: M4. Trace status: PARTIAL_POC.

> BR-FIN-03-05
> ลำดับการเลือกราคา: จำเพาะสิทธิ์+ประเภทผู้ป่วย+สถานที่ → สิทธิ์+ประเภทผู้ป่วย → สิทธิ์ → ราคาทั่วไป (default) และต้องมีราคาทั่วไปเสมอ

## BR-FIN-03-08

Source: B2189, table row 9. Planned milestone: M4. Trace status: PARTIAL_POC.

> BR-FIN-03-08
> ห้ามลบ charge_item_definition ที่เคยถูกอ้างโดย charge_item — ให้ปิดช่วงเวลาแทน (สอดคล้อง BR-CORE-16)

## VR-FIN-03-01

Source: B2193, table row 2. Planned milestone: M4. Trace status: PARTIAL_POC.

> VR-FIN-03-01
> ราคา ≥ 0 ทศนิยม 2 ตำแหน่ง · valid_from < valid_to

## VR-FIN-03-02

Source: B2193, table row 3. Planned milestone: M4. Trace status: PARTIAL_POC.

> VR-FIN-03-02
> ต้องมี charge_item_definition ที่เป็นราคาทั่วไปอย่างน้อย 1 แถวสำหรับทุก catalog_item.is_billable = true

## BR-CORE-18

Source: B0193. Planned milestone: M4/M5. Trace status: SELECTED.

> BR-CORE-18 เจ้าหน้าที่การเงินต้องออกใบเสร็จได้โดยไม่ต้องเข้าถึงเนื้อหาเวชระเบียน — charge_item ต้องมีชื่อรายการที่พอสำหรับออกบิลโดยไม่เปิดเผยการวินิจฉัย

## BR-FIN-01-03

Source: B2088, table row 4. Planned milestone: M4/M5. Trace status: SELECTED.

> BR-FIN-01-03
> ห้ามคอลัมน์วินิจฉัยหรือ FK ไปยัง condition ใน charge_item — ชื่อที่ใช้ออกบิลต้องมาจาก catalog_item.name_th และต้องมีฟิลด์ billing_label แยกกรณีชื่อทางคลินิกเปิดเผยโรค (บังคับ BR-CORE-18)

## BR-FIN-02-10

Source: B2141, table row 11. Planned milestone: M4/M5. Trace status: SELECTED.

> BR-FIN-02-10
> หน้าจอทุกจอในโมดูลนี้ต้องไม่แสดง condition, observation หรือรายละเอียดคำสั่งการรักษา (BR-CORE-18 / BR-ROLE-02)

## BR-CORE-04

Source: B0157. Planned milestone: M5. Trace status: BLOCKED_AMBIGUITY.

> BR-CORE-04 encounter.status = discharged หมายถึงผู้ป่วยออกจากสถานพยาบาลแล้วแต่งานเอกสาร/การเงินยังไม่จบ — completed คือจบทุกอย่าง ทั้งสองสถานะต้องแยกกัน

## BR-FIN-02-06

Source: B2141, table row 7. Planned milestone: M5. Trace status: BLOCKED_AMBIGUITY.

> BR-FIN-02-06
> encounter.status เปลี่ยนเป็น completed ได้เมื่อ account ปิดยอดครบเท่านั้น — discharged แต่ยังค้างเงินให้คงสถานะ discharged (BR-CORE-04)

## BR-FIN-02-12

Source: B2141, table row 13. Planned milestone: M5. Trace status: BLOCKED_AMBIGUITY.

> BR-FIN-02-12
> ผู้ป่วยที่ไม่ชำระต้องปิด encounter ได้ โดยยอดคงค้างย้ายเข้าลูกหนี้ ไม่ใช่ค้าง encounter ไว้ตลอดไป

## BR-CORE-19

Source: B0193. Planned milestone: M5. Trace status: OUT_OF_SCOPE.

> BR-CORE-19 การปิด encounter ทางการเงินยิง event encounter.checkout ไปยัง Next Account Posting Engine เพื่อออก JE — OmniMed ไม่ทำบัญชีเอง

## BR-FIN-02-05

Source: B2141, table row 6. Planned milestone: M5. Trace status: OUT_OF_SCOPE.

> BR-FIN-02-05
> การปิด encounter ทางการเงินต้องยิง encounter.checkout ในธุรกรรมเดียวกับการออกใบเสร็จ (BR-CORE-19) — OmniMed ไม่บันทึกบัญชีเอง

## BR-ROLE-01

Source: B0130. Planned milestone: M0/M5. Trace status: PARTIAL_POC.

> BR-ROLE-01 สิทธิ์เป็นแบบ deny-by-default — ทุกบทบาทต้องถูกกำหนดสิทธิ์อย่างชัดแจ้ง

## BR-ROLE-02

Source: B0130. Planned milestone: M0/M5. Trace status: PARTIAL_POC.

> BR-ROLE-02 บทบาทฝ่ายสนับสนุน (R-FIN, R-INV, R-ADMIN, R-MGR) ต้องไม่สามารถอ่านเนื้อหาเวชระเบียนได้ในทุกกรณี — บังคับที่ชั้น RLS ไม่ใช่ชั้น UI

## BR-ROLE-03

Source: B0130. Planned milestone: M0/M5. Trace status: PARTIAL_POC.

> BR-ROLE-03 R-LAB ถูกจำกัดขอบเขตตาม test_section ที่สังกัด (ตามรูปแบบ system_user_section ของ OpenELIS)

## BR-PLT-01-01

Source: B2905, table row 2. Planned milestone: M0/M5. Trace status: PARTIAL_POC.

> BR-PLT-01-01
> สิทธิ์เป็น deny-by-default (BR-ROLE-01) และการปฏิเสธตาม BR-ROLE-02 มีลำดับสูงกว่าการอนุญาตทุกกรณี — บทบาท R-FIN, R-INV, R-ADMIN, R-MGR อ่าน observation, condition, note ไม่ได้แม้จะถูกเพิ่มบทบาทอื่น

## BR-PLT-01-03

Source: B2905, table row 4. Planned milestone: M0/M5. Trace status: PARTIAL_POC.

> BR-PLT-01-03
> R-ADMIN ตั้งสิทธิ์ให้ตนเองอ่านเวชระเบียนไม่ได้ และการเปลี่ยนสิทธิ์ของตนเองต้องมีผู้อนุมัติคนที่สอง (four-eyes)

## BR-PLT-01-08

Source: B2905, table row 9. Planned milestone: M0/M5. Trace status: PARTIAL_POC.

> BR-PLT-01-08
> ห้ามใช้บัญชีร่วม (shared account) สำหรับการกระทำทางคลินิก — อุปกรณ์ร่วม (kiosk, จอ, เครื่องวิเคราะห์) ใช้ device credential แยกประเภทที่กระทำการทางคลินิกไม่ได้

## VR-PLT-01-02

Source: B2909, table row 3. Planned milestone: M0/M5. Trace status: PARTIAL_POC.

> VR-PLT-01-02
> ผู้ใช้ต้องมีอย่างน้อย 1 บทบาทที่ active จึงจะล็อกอินได้

## VR-PLT-01-06

Source: B2909, table row 7. Planned milestone: M0/M5. Trace status: PARTIAL_POC.

> VR-PLT-01-06
> ผู้ใช้ที่มีบทบาท R-LAB ต้องระบุ test_section อย่างน้อยหนึ่งค่า (BR-ROLE-03)

## NFR-S-01

Source: B0256, table row 2. Planned milestone: M0/M5. Trace status: DEFERRED.

> NFR-S-01
> บังคับสิทธิ์ด้วย RLS สองชั้นที่ฐานข้อมูล ไม่พึ่งชั้นแอปพลิเคชันเพียงอย่างเดียว

## NFR-S-02

Source: B0256, table row 3. Planned milestone: M0/M5. Trace status: DEFERRED.

> NFR-S-02
> เข้ารหัสข้อมูลอ่อนไหวระดับฟิลด์ด้วย AES-256 คีย์แยกต่อผู้เช่า และหมุนคีย์ได้โดยไม่ต้องหยุดระบบ

## BR-PLT-01-02

Source: B2905, table row 3. Planned milestone: M0/M5. Trace status: DEFERRED.

> BR-PLT-01-02
> บริบทสิทธิ์ต้องถูกส่งเข้า session ของฐานข้อมูล (SET LOCAL) ทุกคำขอ และนโยบาย RLS เป็นผู้บังคับจริง — ชั้นแอปพลิเคชันเป็นเพียงการซ่อน UI

## NFR-S-03

Source: B0256, table row 4. Planned milestone: M5. Trace status: PARTIAL_POC.

> NFR-S-03
> บันทึก audit ทุกการเข้าถึงข้อมูลผู้ป่วย รวมถึงการอ่าน (SELECT) ผ่านฟังก์ชันที่กำหนด เก็บ 5 ปี

## NFR-S-04

Source: B0256, table row 5. Planned milestone: M5. Trace status: PARTIAL_POC.

> NFR-S-04
> audit log ต้อง append-only และผู้ดูแลระบบต้องลบหรือแก้ไม่ได้

## NFR-Q-01

Source: B0260, table row 2. Planned milestone: M5. Trace status: PARTIAL_POC.

> NFR-Q-01
> ทุกระเบียนทางคลินิกต้องระบุได้ว่าใครสร้าง ใครแก้ เมื่อใด และแก้อะไร (field-level history)

## BR-CLI-01-09

Source: B0558, table row 10. Planned milestone: M5. Trace status: PARTIAL_POC.

> BR-CLI-01-09
> ทุกการเปิดอ่านเวชระเบียนยิง phi.accessed รวมถึงการอ่านผ่าน API และการพิมพ์ (NFR-S-03)

## BR-PLT-04-01

Source: B3050, table row 2. Planned milestone: M5. Trace status: PARTIAL_POC.

> BR-PLT-04-01
> ทุกการอ่านข้อมูลผู้ป่วย รวมถึง SELECT ต้องถูกบันทึก audit ผ่านฟังก์ชันที่กำหนด และเก็บอย่างน้อย 5 ปี (NFR-S-03) — ไม่มีเส้นทางอ่านที่ไม่ผ่านการบันทึก

## BR-PLT-04-02

Source: B3050, table row 3. Planned milestone: M5. Trace status: PARTIAL_POC.

> BR-PLT-04-02
> audit log เป็น append-only ที่ระดับฐานข้อมูล — R-ADMIN แก้หรือลบไม่ได้ (NFR-S-04) และการเข้าถึง audit เองก็ถูกบันทึก

## BR-PLT-04-10

Source: B3050, table row 11. Planned milestone: M5. Trace status: PARTIAL_POC.

> BR-PLT-04-10
> ทุกการส่งออกข้อมูลผู้ป่วยออกนอกระบบ (พิมพ์ ดาวน์โหลด API export) ต้องบันทึกเป็นเหตุการณ์ประเภท disclosure แยกจากการอ่านทั่วไป เพื่อรายงานต่อเจ้าของข้อมูลได้

## BR-PLT-04-13

Source: B3050, table row 14. Planned milestone: M5. Trace status: PARTIAL_POC.

> BR-PLT-04-13
> audit ต้องบันทึกอย่างน้อย: ผู้กระทำ บทบาทที่ใช้ ผู้ป่วยที่ถูกเข้าถึง ทรัพยากร การกระทำ ผลลัพธ์ เวลา (แหล่งเวลาที่ซิงก์) IP/อุปกรณ์ และเหตุผลกรณี break-glass

## BR-PLT-05-01

Source: B3101, table row 2. Planned milestone: M5. Trace status: PARTIAL_POC.

> BR-PLT-05-01
> FHIR R4 (4.0.1) เป็นรูปแบบภายในและรูปแบบที่ให้บริการหลัก — R5 ทำเป็น adapter ขาออกเท่านั้น ห้ามเก็บข้อมูลสองรูปแบบคู่ขนาน (A-01)

## BR-PLT-05-03

Source: B3101, table row 4. Planned milestone: M5. Trace status: PARTIAL_POC.

> BR-PLT-05-03
> ทุกคำขอที่อ่านข้อมูลผู้ป่วยต้องยิง phi.accessed และบันทึก AuditEvent ตาม BALP pattern พร้อม entity ที่อ้าง Patient

## BR-PLT-05-12

Source: B3101, table row 13. Planned milestone: M5. Trace status: PARTIAL_POC.

> BR-PLT-05-12
> CapabilityStatement ต้องถูกสร้างจากความสามารถจริงของระบบ ไม่ใช่เอกสารที่เขียนมือ เพื่อไม่ให้คลาดจากพฤติกรรมจริง

## VR-PLT-05-02

Source: B3105, table row 3. Planned milestone: M5. Trace status: PARTIAL_POC.

> VR-PLT-05-02
> รหัสใน CodeableConcept ต้องอยู่ใน ValueSet ที่ binding กำหนดเมื่อ binding เป็น required

## VR-PLT-05-04

Source: B3105, table row 5. Planned milestone: M5. Trace status: PARTIAL_POC.

> VR-PLT-05-04
> คำขอที่ไม่มี Authorization ที่ถูกต้องต้องคืน 401 และไม่เปิดเผยว่ามีทรัพยากรนั้นอยู่หรือไม่

