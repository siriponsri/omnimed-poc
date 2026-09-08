# Local runtime and validation

Docker Compose เป็น authoritative runtime. ต้องใช้ Docker Compose >=2.24.4 (full smoke ใช้ `!override`), Python 3.12; native checks ใช้ uv และ Node 24.20.x. Windows ใช้ PowerShell + Docker Desktop Linux containers; `python` ใช้ executable Python 3.12 ของคุณ. ไม่ต้องมี Make, Railway, OpenRouter หรือ plugin

## One command และ environment

จาก repo root: `python scripts/dev.py up`. Script สร้าง `.env` เฉพาะเมื่อยังไม่มี แล้ว `docker compose config --quiet` และ `up --build --detach --wait --wait-timeout 180`. หาก build สำเร็จแต่สุขภาพยังไม่พร้อม ตรวจ `python scripts/dev.py logs` แล้วแก้สาเหตุ; ไม่ลบ volume เพื่อกลบ migration error

| Variable | Local source/default | ความหมาย |
|---|---|---|
| POSTGRES_USER | `.env`, omnimed | Local DB user |
| POSTGRES_PASSWORD | init สุ่ม 48 hex chars | Required; ไม่ commit; Compose ประกอบ DSN จากค่านี้ จึงใช้ hex เพื่อหลีกเลี่ยง URL escaping |
| POSTGRES_DB | omnimed_demo | Synthetic demo DB; ไม่ใช้ชื่อ test |
| APP_ENV | local | local/test/demo; demo ต้อง acknowledgement |
| SYNTHETIC_DEMO_ONLY | true | Demo acknowledgement; ไม่ใช่ PHI detector |
| DATABASE_URL | Compose สร้างภายใน backend | Native mode ต้องกำหนด PostgreSQL DSN เอง; ดู `.env.example` |
| API_INTERNAL_URL | http://backend:8000 ใน Compose | Next server → API; native default http://127.0.0.1:8000 |
| PORT | backend 8000 / frontend 3000 | Backend ตรวจ integer 1–65535; ไม่เปลี่ยน host ports ให้อัตโนมัติ |
| OMNIMED_TEST_DATABASE_URL | ไม่มี default | เฉพาะ opt-in integration test บน empty omnimed_test[_suffix] DB |

`.env` ไม่ถูกโหลดอัตโนมัติใน native Python commands. Compose โหลดเอง; หากรัน native ให้ export ตัวแปรใน shell ของคุณ. ตัวอย่างนี้ใช้ชื่อ database/username สังเคราะห์และ placeholder password ต้องแทนด้วยค่าท้องถิ่น ห้าม paste ค่า secret ไป issue/log

## Migration / seed

Compose ทำ migrate → seed ก่อนเปิด API โดยอัตโนมัติ. รันซ้ำเพื่อตรวจได้:

```sh
docker compose run --rm migrate
docker compose run --rm seed
docker compose exec backend alembic -c db/alembic.ini current
```

Seed ไม่ truncate หรือ overwrite; insert และตรวจ fixture ใน transaction เดียว. ถ้าพบ fixture ถูกแก้จะ fail และ rollback. คืนค่าข้อมูลจากการตรวจสอบอย่างตั้งใจ ห้ามแก้ seed ให้ข้าม conflict. `downgrade base` ใช้กับ disposable test DB เท่านั้น เพราะลบ foundation tables

## Native development

```sh
uv sync --frozen --extra dev
cd frontend
npm ci
cd ..
```

ใช้ PostgreSQL 17 ที่ติดตั้งเองหรือเปิดเฉพาะ service: `python scripts/dev.py init` แล้ว `docker compose up -d db`. ตั้ง `DATABASE_URL` ให้ชี้ localhost และใช้ secret ใน `.env`. Bash:

```sh
export APP_ENV=local
export DATABASE_URL='postgresql+psycopg://omnimed:REPLACE_WITH_LOCAL_PASSWORD@127.0.0.1:5432/omnimed_demo'
uv run alembic -c db/alembic.ini upgrade head
uv run python scripts/seed_demo.py
uv run python scripts/start_backend.py
```

PowerShell ใช้ `$env:APP_ENV='local'` และ `$env:DATABASE_URL='postgresql+psycopg://omnimed:REPLACE_WITH_LOCAL_PASSWORD@127.0.0.1:5432/omnimed_demo'` แล้วคำสั่ง uv เหมือนกัน. เปิด terminal อีกหน้ารัน `npm run dev` ใน frontend; [localhost:3000](http://localhost:3000). Production native check ใช้ `npm run build` แล้ว `npm run start`; Docker ใช้ standalone `node server.js` จาก image

## Health contract

| Endpoint | Expected | ตรวจอะไร |
|---|---|---|
| GET backend /api/health/live | 200 alive | Process ยังตอบได้ ไม่แตะ DB |
| GET backend /api/health/ready | 200 ready / 503 not_ready | PostgreSQL reachable, exact Alembic revision และตาราง M0 ครบ |
| GET frontend / | 200 | Frontend shell เปิดได้ |
| GET frontend /api/status | 200 ready / 503 unavailable | Server-side readiness proxy; ไม่ส่ง DSN/driver error ให้ browser |

Readiness ไม่รับรอง clinical safety, auth, seed count หรือ feature completeness. Migration/seed exit code และ tests ตรวจเงื่อนไขคนละส่วน

## Deterministic gates

`python scripts/checks.py` รัน available non-Docker gates และบันทึก commands/exit codes. `python scripts/checks.py --full` ต้องมี Docker daemon และ Chromium (`cd frontend` แล้ว `npx playwright install --with-deps chromium`). Full gate ทำงานผ่าน `scripts/compose_smoke.py` โดยเลือก random project, random loopback host ports และแยก test DB; ลบเฉพาะสิ่งที่สร้างสำหรับการทดสอบ

หากต้องรัน migration test แยก ให้สร้าง **empty disposable** DB ชื่อ `omnimed_test` หรือ `omnimed_test_...` ตั้ง `OMNIMED_TEST_DATABASE_URL` แล้ว `uv run pytest backend/tests/integration -q`. Test ปฏิเสธชื่ออื่นหรือตาราง public ที่มีอยู่; test downgrade/drop เฉพาะ fixture ของตน. การขาด env จะ SKIP ซึ่งไม่ใช่ PASS

ใน Work environment ที่ใช้สร้าง candidate นี้ไม่มี Docker daemon และไม่มี live PostgreSQL ที่รันได้. จึงตรวจ Compose syntax ด้วย standalone Compose binary แต่ยังไม่รัน stack/migration จริง. ห้ามนำผล unit/mock tests มาแทนรายการนี้. ดู `validation/` สำหรับผลล่าสุด และให้ M0-01 รันเต็มบน workstation/CI ก่อนยอมรับ release
