# ADR-0002 — Order revision versus lifecycle updates

Status: PROPOSED / BLOCKED_AMBIGUITY · Sources: BR-CORE-12/14, BR-CLI-02-02 · Finding SG-002

SRS ต้องการ revoke predecessor และสร้าง revision ใหม่ แต่เขียนห้าม UPDATE เดิมกว้างจน lifecycle transition ไม่ชัดเจน. Candidate: clinical payload immutable; revision/discontinue แถวใหม่ link previous_order_id; lifecycle status update อนุญาตผ่าน service ที่ append history actor/time/reason ใน transaction เดียว และควบคุม stale revision

ยังไม่ได้รับ semantic approval. ทางเลือก append-only state events ทั้งหมดต้องอธิบาย mapping ว่า revoked predecessor ตรง SRS อย่างไรและมี read projection ใด. ห้าม Builder เลือกเองโดยเงียบ. M3-00 ต้อง freeze decision, trace และ AT-REV ก่อน M3-02. ไม่มี Order code ใน M0 จึงไม่เกิดการแก้ clinical history ตอนนี้
