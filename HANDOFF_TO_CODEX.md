# ส่งต่อ Codex — OmniMed POC v0.1

รอบ Work สร้าง M0 เท่านั้น. เปิด `validation/FINAL_DELIVERY_REPORT.md` ก่อนเพื่อดู gates ที่รันจริงและข้อจำกัด environment; อย่าถือว่า full Docker/PostgreSQL/E2E ผ่านจากคำว่า starter

## เริ่มในเครื่อง

1. แตก ZIP แล้วเปิดโฟลเดอร์ `omnimed-poc` ใน VS Code/Codex
2. เปิด Docker Desktop (Linux containers); `python scripts/dev.py up` สร้าง .env ครั้งแรกและเริ่ม local stack
3. เปิด `http://localhost:3000`; เลือกบทบาทสำรวจหน้าจอ และกดตรวจสถานะโครงระบบ
4. ถ้าเครื่ององค์กรยังไม่มี Docker ให้ใช้เครื่องที่ IT อนุมัติหรือเครื่องส่วนตัว. Portable Node ใช้ทำ frontend ได้ แต่ไม่แทน PostgreSQL/Docker. ไม่เปลี่ยนนโยบายเครื่องเพื่อให้ติดตั้งผ่าน
5. Developer dependencies: `uv sync --frozen --extra dev`, แล้ว `cd frontend` และ `npm ci`; กลับ root รัน `python scripts/checks.py`

ก่อน M1 ทำ docs/tasks/M0-01.md เพื่อปิด environment validation ด้วย `docs/LOCAL_VALIDATION.md`. Native path ใช้ PostgreSQL ที่เตรียมไว้; ไม่ทดแทนด้วย SQLite

## Prompt แรกสำหรับ Codex

```text
อ่าน AGENTS.md, docs/POC_CONTRACT.md, .ai/TASK_TEMPLATE.md,
docs/tasks/M1-01.md และ exact excerpts ที่ task อ้าง
ตรวจ validation/FINAL_DELIVERY_REPORT.md และปิด M0 environment gates ที่ยัง NOT_RUN
บนเครื่องที่มี Docker/PostgreSQL ก่อนเปลี่ยน schema
จากนั้น implement เฉพาะ M1-01: Party/Patient/PatientIdentifier persistence
พร้อม self relation, generated HN concurrency และ migration/tests
ห้ามทำ registration UI, Encounter, clinical endpoint หรือ M2–M5 ใน task นี้
ใช้ Builder → deterministic gates → read-only SRS Guardian → Reviewer
จำกัด repair loops ตาม AGENTS.md; update trace และ changed-file evidence
ห้ามใช้ paid API, จริง PHI หรือเพิ่ม LLM เข้า product runtime
ถ้า gate ทำไม่ได้ให้รายงาน evidence/ข้อจำกัด ห้ามแทน NOT_RUN ด้วย PASS
```

## จุดที่ยังต้องตัดสินใจก่อน feature ที่เกี่ยวข้อง

- ก่อน M3: ADR-0002 revision payload/history interpretation; ไม่เปลี่ยนคำสั่งเดิมจนประวัติหาย
- ก่อน M4: ADR-0003 lab technical_complete/release timing และ single-operator demo configuration
- ก่อน M5 completion: SG-003/004 principal diagnosis + signed note และวิธีปิดยอดบัญชีสังเคราะห์. ไม่ถือว่า charge=paid
- เอกสาร Next Account/legacy ADR/schema ยังไม่พร้อม; ไม่เริ่ม real adapter หรือ JE

API/model configuration อยู่ใน `.ai/`; v0.1 ไม่มี live OpenRouter adapter. อ่าน ROUTING_POLICY ก่อนเปิดงาน integration รอบใหม่. `FakeProvider` ใช้ทดสอบ interface เท่านั้นและไม่สามารถผ่าน release gate
