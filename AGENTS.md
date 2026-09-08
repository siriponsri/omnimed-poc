# OmniMed coding contract

อ่านตามลำดับ: `docs/POC_CONTRACT.md` → `.ai/TASK_TEMPLATE.md` → task ปัจจุบันใน `docs/tasks/` → relevant excerpts ใน `docs/source/SELECTED_SRS_EXCERPTS.md` → changed files. ไม่อ่าน SRS ทั้งฉบับทุกรอบ

## Authority and scope

Explicit user/master prompt > SRS v2.0 domain/business rules > frozen POC contract > UI reference > course routing > external references > intuition. M0 release นี้มี foundation เท่านั้น. งานใหม่เริ่มด้วย task contract เดียว; ห้ามเปลี่ยน task เป็น “build whole HIS”. ใช้ exact SRS IDs และ body/table locators; mockup IDs ไม่ใช่ authority

ห้ามเพิ่ม IPD/OR/CDS/real government integration/stock/production deployment/microservices. Railway demo configuration ได้รับอนุญาตตาม D01; ใช้ Dockerfiles เดียวกับ local และข้อมูลสังเคราะห์เท่านั้น. ห้ามเอา LLM เข้า request path. ห้ามเพิ่ม paid dependency หรือเรียก model ใน tests. Architecture/invariant change ต้องมี ADR; ถ้าขัด SRS หรือขยาย scope โดยยังไม่มี explicit authorization ให้ block เฉพาะ task นั้น

## Code and data

Python 3.12, FastAPI, Pydantic, SQLAlchemy 2, Alembic, PostgreSQL; Next.js/TypeScript strict. Preserve lockfiles. Run formatting/lint; no broad refactor unrelated to task. ไม่มี fake success, dummy endpoint, hardcoded health=ready, fake compliance badge หรือ test ที่ skip แล้วรายงานว่าผ่าน

Clinical values → Observation, Orders → Encounter, revisions preserve immutable payload/history, no clinical hard delete. Tenant/actor fields on patient tables; UTC timestamps with explicit zone at display. Foreign keys involving patient data must prevent cross-tenant links, not just add tenant_id columns. Domain modules own writes; cross-module state transitions use transactional outbox contract. No duplicated drug/lab order roots

ทุก protected route ที่เพิ่มต้องมี deny-by-default authorization, negative permission tests และ protected-read audit ตั้งแต่ task นั้น. R-FIN/R-ADMIN clinical denial wins even for mixed roles. UI role preview has no authentication meaning. Synthetic data only; no citizen IDs, secrets, screenshots or PHI from real systems. Do not log clinical bodies/tokens/DB URLs

## Migrations

Never use metadata.create_all in product startup. New versioned Alembic migration, explicit upgrade/downgrade, reviewed SQL and real PostgreSQL test. No destructive downgrade against user databases. Integration test accepts only an empty disposable omnimed_test[_suffix] DB. It drops its own schema at test end. Seed idempotently in one transaction; migrations and seeds fail closed

## Required gates

```sh
uv sync --frozen --extra dev
uv run python scripts/backend_checks.py
python scripts/checks.py
# Full gate on an equipped machine; creates its own disposable PostgreSQL test DB:
python scripts/checks.py --full
```

`NOT_RUN` and `SKIP` never equal PASS. Evidence includes command, exit code, scope, limitations and candidate hash. Readiness failure must return 503 without diagnostic secrets. Add meaningful domain/permission/idempotency tests as features arrive; don't expand coverage solely for percentages

## Four roles and repair limits

Orchestrator owns task/route/evidence; Builder edits; SRS Guardian reads only and returns PASS/FAIL/UNCERTAIN with SRS citations; Reviewer checks quality/security/UX. Builder → deterministic gates → Guardian → Reviewer. Two normal repair loops, three hard-blocker loops; rerouting does not reset the counter. Then BLOCKED_REQUIRES_HUMAN. No swarm, recursive delegation or external API by default

## Definition of done

Task acceptance, deterministic gates and both reviews pass on the same candidate. Requirement trace and relevant docs updated. Changed files and tests reported; future behavior clearly NOT_IMPLEMENTED. Close findings with evidence, not a claim. Preserve source snapshots. Never mark an M1–M5 milestone complete based on M0 tests. Configuration for deployment is authorized; actual publish/provisioning needs an explicit deployment request

## Mandatory skill routing

Repository skills live under `.agents/skills/`.

Skills supplement this contract; they never override:
user instruction > selected SRS requirement > POC contract > current task.

For any code implementation:
- use `karpathy-guidelines`
- use `tdd` when behavior can be expressed through automated tests

For database/domain boundary changes:
- use `codebase-design`
- consult `omnimed-srs-guardian` before declaring the task complete

For bug investigation:
- use `diagnosing-bugs`

Before task completion:
- use `code-review`

Frontend/design skills are not invoked for backend-only tasks unless the
task explicitly changes UI behavior.

Read only the selected SKILL.md and the references it requires.
Do not load every installed skill into context.