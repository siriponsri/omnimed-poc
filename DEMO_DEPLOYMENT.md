# Railway demo deployment from GitHub

Local/on-premise ใช้ Docker Compose เป็น authoritative architecture. Railway เป็น optional synthetic demo: frontend Next.js + backend FastAPI modular monolith + PostgreSQL หนึ่งฐาน ใช้ Dockerfiles เดิม ไม่มี Railway dependency ใน product runtime และไม่มี production PHI

**สถานะ:** config/type tests รันใน Work ได้; ยังไม่มี Railway project, plan/apply หรือ live deployment ที่ตรวจแล้ว. ต้องปิด local runtime gate M0-01 ก่อนยอมรับ release. M0 เปิดดู shell/health เท่านั้น ไม่มี login, patient input, clinical endpoint หรือสิทธิ์จริงจาก role selector

## ทำไมไม่มี railway.toml / railway.json

เอกสาร Railway ที่ตรวจเมื่อ 2026-09-08 ระบุ config-as-code เดิม deprecated และ service ใหม่ opt in ไม่ได้แล้ว จึงใช้ `.railway/railway.ts` สำหรับ Infrastructure as Code แทน. SDK อยู่เฉพาะ optional tooling พร้อม lockfile; dashboard setup ด้านล่างใช้ได้โดยไม่ต้องเรียก IaC. อย่าเปิด legacy Config File ควบคู่กับ IaC. [Railway IaC](https://docs.railway.com/infrastructure-as-code)

## เตรียม GitHub และ dedicated demo

1. นำโฟลเดอร์ repo นี้เป็น root ของ GitHub repository ที่คุณมีสิทธิ์ เช่น `OWNER/omnimed-poc`, branch `main`. Commit source/lockfiles เท่านั้น ไม่ commit `.env`, database dumps, model keys หรือ node_modules. Binary SRS/mockup ไม่อยู่ใน package; review excerpts ยังมี source rights จึงใช้ private repo จนตรวจสิทธิ์เผยแพร่
2. ให้ GitHub CI รัน `python scripts/checks.py --full` ผ่านบน Linux Docker runner. Workflow ที่ให้มาไม่ deploy และไม่ต้องมี Railway token
3. ใน Railway สร้าง dedicated project/environment ชื่อ `demo`. ใช้ environment ใหม่ที่มี IPv4 private networking; starter backend bind `0.0.0.0`. อย่านำไปใช้กับ legacy IPv6-only private environment โดยไม่ปรับและทดสอบ network binding ตาม [private-network library configuration](https://docs.railway.com/networking/private-networking/library-configuration)
4. เชื่อม Railway GitHub App กับ repository นี้ แล้วเลือกวิธี IaC หรือ dashboard ด้านล่าง. Resource provisioning อาจมีค่าใช้จ่ายของ Railway; local runtime ไม่พึ่งบัญชีนี้

## วิธี A — Infrastructure as Code

ติดตั้ง Railway CLI >=5.42.1 ตาม [official CLI installation](https://docs.railway.com/guides/cli) และใช้ Node 24.20.x. ใช้ linked project ที่แยกสำหรับ demo เท่านั้น; file นี้อธิบายทั้ง environment จึงต้อง review plan ก่อน apply

```sh
cd .railway
npm ci
npm run typecheck
npm test
cd ..
railway login
railway link
```

เลือก project และ environment `demo` ตอน link. ตั้ง repository ที่แท้จริงใน shell ซึ่งใช้ประเมิน config (ไม่ใช่ backend variable):

```sh
# Bash
export OMNIMED_GITHUB_REPOSITORY='OWNER/omnimed-poc'
railway config plan
# หลังตรวจว่ามีเพียง demo resources ที่ตั้งใจสร้าง/เปลี่ยน
railway config apply
```

PowerShell ใช้ `$env:OMNIMED_GITHUB_REPOSITORY='OWNER/omnimed-poc'` แล้ว plan/apply เหมือนกัน. Config ปฏิเสธ environment อื่นและ missing/invalid repository. CLI ประเมิน file; การ push source อย่างเดียวไม่ได้ apply การแก้ topology. หลังเชื่อม source แล้ว GitHub autodeploy ใช้ branch `main`; ตรวจให้ deploy เฉพาะ commit ที่ CI ผ่าน. [IaC workflow](https://docs.railway.com/infrastructure-as-code), [GitHub autodeploys](https://docs.railway.com/guides/github-autodeploys)

IaC สร้าง intent ของ Postgres พร้อม private reference และ Docker services backend/frontend. SDK 3.11.0 ใช้ Railway Postgres template 18; local Compose pin 17.11. Domain/schema เดียวกัน; live compatibility ของทั้งสอง target ยังต้องตรวจใน deployment gate. อย่าเปลี่ยน PostgreSQL major version ของฐานเดิมโดยการเปลี่ยน image tag; ใช้ migration/upgrade procedure ของฐานนั้น

หลัง services healthy ให้สร้าง Railway-generated public domain **เฉพาะ frontend port 3000** ใน Settings → Networking. Backend/Postgres ใช้ private network ไม่สร้าง public HTTP/TCP endpoint สำหรับ demo นี้. Generated domain ตั้งผ่าน dashboard ไม่ hard-code ใน IaC

## วิธี B — Dashboard พร้อม GitHub source

สร้าง PostgreSQL service ชื่อ `Postgres` ก่อน แล้วสร้าง 2 services จาก **GitHub repository เดียวกัน**. ตั้ง root directory เป็น `/` ทั้งคู่ เพราะ backend ต้องอ่าน root pyproject/uv.lock/db และ Dockerfiles ใช้ repo root เป็น build context. อย่าตั้ง root เป็น backend หรือ frontend

| Setting | backend | frontend |
|---|---|---|
| Source / branch | GitHub repo / main | GitHub repo / main |
| Root directory | / | / |
| Builder | Dockerfile | Dockerfile |
| Dockerfile path | backend/Dockerfile | frontend/Dockerfile |
| Start command | python scripts/start_backend.py | node server.js |
| Pre-deploy | alembic -c db/alembic.ini upgrade head && python scripts/seed_demo.py | ไม่มี |
| Health path | /api/health/ready | / |
| Health timeout | 120 seconds | 120 seconds |
| Replicas | 1 | 1 |
| Restart policy | on failure, maximum 3 retries | on failure, maximum 3 retries |
| Public networking | ไม่มี | generated HTTPS domain → port 3000 |

หาก UI ไม่มี Dockerfile path field ให้ตั้ง Railway build variable `RAILWAY_DOCKERFILE_PATH` เป็น path ในตาราง. ไม่ใช้ Railpack/Nixpacks สำหรับ app services นี้. [Dockerfile configuration](https://docs.railway.com/guides/dockerfiles)

## Environment variables

ค่า `${{...}}` ด้านล่างเป็น Railway variable reference ที่กรอกใน dashboard ไม่ใช่ shell expansion. IaC สร้าง references เหล่านี้ผ่าน SDK อยู่แล้ว

| Service | Variable | Value / source | Required |
|---|---|---|---|
| backend | APP_ENV | demo | yes |
| backend | SYNTHETIC_DEMO_ONLY | true (exact lowercase) | yes; startup rejects missing/false |
| backend | DATABASE_URL | `${{Postgres.DATABASE_URL}}` (private URL) | yes, secret reference |
| backend | PORT | 8000 | yes in supplied config |
| frontend | NODE_ENV | production | yes |
| frontend | HOSTNAME | 0.0.0.0 | yes |
| frontend | PORT | 3000 | yes in supplied config |
| frontend | NEXT_TELEMETRY_DISABLED | 1 | yes in supplied config |
| frontend | API_INTERNAL_HOST | `${{backend.RAILWAY_PRIVATE_DOMAIN}}` | yes |
| frontend | API_INTERNAL_PORT | 8000 | yes |
| frontend | API_INTERNAL_URL | omit; optional full private URL overrides host/port | optional |
| authoring shell only | OMNIMED_GITHUB_REPOSITORY | actual OWNER/repo | IaC only |

Railway manages DB credentials. Do not copy local `.env` or use `DATABASE_PUBLIC_URL` in backend. Accepted backend URL schemes: `postgres://`, `postgresql://`, `postgresql+psycopg://`; config normalizes to psycopg preserving escaped credentials/query parameters. PORT must be ASCII integer 1–65535. No NEXT_PUBLIC database secret, CORS workaround, OpenRouter key or LLM endpoint is needed

## Migration / seed / start

Pre-deploy executes these in order in the **built backend image** with its private database environment:

```sh
alembic -c db/alembic.ini upgrade head
python scripts/seed_demo.py
```

Dashboard single command uses `&&` so seed runs only after migration succeeds; IaC uses Railway's ordered pre-deploy command list. A failed command blocks the new deployment. Do not run migration while building the image: build has no runtime DB context. Pre-deploy container files/volumes do not persist; this seed writes transactionally to PostgreSQL only. [Pre-deploy behavior](https://docs.railway.com/guides/pre-deploy-command)

Start: backend `python scripts/start_backend.py`; frontend standalone `node server.js`. Images contain the installed app/CLI and lockfile-resolved dependencies. No runtime `npm install`, `uv sync` or external model request

To reseed manually, open a Railway SSH shell for the backend service in `demo`, then `python scripts/seed_demo.py`. Repeated seed must preserve the same 1 tenant + 7 roles + 7 non-login identities. A conflicting fixture fails rather than silently overwriting. There are **no patient records/passwords** in this seed. `SYNTHETIC_DEMO_ONLY=true` is an operator acknowledgement, not a PHI detector. Never import a production database or add real patient data through SQL

## Verify the deployed demo

| Check | Expected |
|---|---|
| Backend health deployment | /api/health/ready returns 200 only after PostgreSQL/revision/tables ready |
| Frontend domain / | 200, M0 demo banner, seven-role preview, clinical actions disabled |
| Frontend domain /api/status | 200 with only `status: ready` |
| Database unavailable | backend live stays 200; ready and frontend status become 503 with sanitized bodies |
| Backend image command `alembic -c db/alembic.ini current` | 0001_foundation |
| Repeated demo seed | same synthetic fixture counts; no patient data created |

Use frontend domain `/api/status` to verify the private dependency path. Frontend `/` health intentionally proves shell availability; database readiness is separate. Do not call it clinical readiness. Railway health checks gate deployment; use an external monitor later if continuous uptime monitoring is needed. [Health checks](https://docs.railway.com/guides/healthchecks)

Retain commit SHA, target/env, build/deploy result, migration revision and sanitized health/seed evidence in a new validation run. Current package does not contain that cloud PASS. For migration/seed error fix the failed cause and redeploy; do not downgrade an existing DB automatically or delete its volume. Code rollback alone does not reverse schema changes; M0 rollback/downgrade tests use disposable data only

## Local architecture remains unchanged

Local `python scripts/dev.py up` still provisions one PostgreSQL database and the same two app images with local migration/seed. `.railway` is excluded from Docker contexts. There is no cloud account, SDK, secret, storage service, broker or hosted auth in the local request path. Future clinical routes must pass deny/audit tests before any revised demo is exposed; production/on-premise hardening remains a separate project scope
