# ADR-0005 — Optional Railway demo from GitHub

Status: ACCEPTED · Basis: later explicit user deployment instruction D01 · 2026-09-08

Local/on-premise Docker Compose ยังคง authoritative. Railway ใช้ backend/frontend Dockerfiles เดิมกับ private PostgreSQL และ public frontend เท่านั้น. Cloud config อยู่ `.railway` ใน tooling layer; ไม่มี cloud imports ใน domain. Migration+synthetic seed เป็น pre-deploy commands; API ใช้ PORT และ normalizes supported PostgreSQL URLs

Railway docs ปัจจุบันแนะนำ TypeScript Infrastructure as Code; legacy railway.toml/json config-as-code เลิกให้บริการใหม่ opt in แล้ว. จึงส่ง `.railway/railway.ts` พร้อม dashboard GitHub steps และ lockfile ของ optional SDK แทน config เก่าที่อาจ deploy ไม่ได้. Typecheck/offline configuration evaluation เป็น local evidence; ไม่อ้างว่า plan/apply/deploy จริงแล้ว

ใช้ dedicated demo environment, APP_ENV=demo และ SYNTHETIC_DEMO_ONLY=true. Backend ปฏิเสธ demo startup หาก acknowledgement ไม่มี. M0 ไม่รับ clinical data; เมื่อเพิ่ม clinical routes ต้อง review cloud exposure ใหม่ตาม task security gates. ไม่มี production PHI และไม่ถือ flag ว่าเป็น PHI detection. ดู DEMO_DEPLOYMENT.md สำหรับ exact commands/health/env
