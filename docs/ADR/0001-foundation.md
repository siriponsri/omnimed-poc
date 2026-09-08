# ADR-0001 — M0 architecture and implementation boundary

Status: ACCEPTED · Basis: explicit master §§5/20 · 2026-09-08

ใช้ Python 3.12/FastAPI/Pydantic/SQLAlchemy/Alembic, Next.js/TypeScript และ PostgreSQL ฐานเดียวใน modular monolith. Compose มี migration/seed one-shots เพื่อให้ error block API startup. Domain tables ใน M1–M5 ยังไม่สร้าง; M0 มี foundation_tenant/role/demo_identity เท่านั้น

ไม่มี plugin, LLM, OpenRouter หรือ broker ใน runtime. ไม่มี mock endpoint ที่อ้าง clinical success. เลือก SQLAlchemy เพราะมี explicit constraints และ Alembic migration story; ไม่ใช้ SQLite แทน PostgreSQL ใน integration tests. ผลคือ starter เรียนรู้/ตรวจได้โดยไม่ต้องสร้าง HIS ทั้งระบบ; clinical acceptance ต้องทำใน tasks ถัดไป
