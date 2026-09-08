# SRS Guardian — backend/database/runtime second gate

Review scope: `backend/app`, backend tests, `db`, backend Dockerfile, Compose configuration, `scripts/dev.py`, seed/backend check scripts and the local check orchestrator. Root is still authoring documents/frontend; their absence or incompleteness is outside this review.

Contract: `docs/POC_CONTRACT.md` C01–C08; user master M0 implementation boundary. No product code changed. This is source/evidence review, not a live PostgreSQL or Docker execution report.

## Review snapshot boundary

This snapshot precedes the new explicit user request for Railway demo-deployable configuration. Root will amend the contract to permit cloud demo configuration only. Planned APP_ENV=demo, PostgreSQL URL normalization and PORT launcher changes require a focused delta review; they are not covered by this source PASS. No deployment has been executed.

## Verdict

**Backend/domain source gate: PASS for the implemented M0 subset.** No Critical or High code defect was found in the reviewed backend, seed or migration source. Clinical domain/authentication behavior is correctly absent.

**Compose/PostgreSQL runtime gate: UNCERTAIN / NOT_RUN.** The environment has neither Docker nor an executable live PostgreSQL service for these checks. The namespace is restricted to the existing root UID. No runtime, persistence, live migration, seed-transaction or actual database-constraint PASS is granted here.

**One Medium verification defect remains in the full-check command:** SG-B01 below. It can be fixed independently of backend functionality and requires no scope expansion.

## SG-B01 — full-check aggregation omits Compose startup

- Severity: **MEDIUM**.
- Location: `scripts/checks.py`, full-mode gate list, especially `compose-config` and the final full-release wording; `scripts/dev.py` already implements `up` and `status` separately.
- Evidence: `--full` adds `python scripts/dev.py config`, the explicit disposable PostgreSQL test, and browser E2E. It never invokes Compose `up`, checks the Compose service states, or probes the built stack. The PostgreSQL integration DSN can point at a separate local server, and the browser suite is not evidence that the Docker images successfully build/start.
- Consequence: all entries in the full-check result can be PASS while Compose images or the startup dependency chain have never executed, even though contract C08 and the user delivery gate require actual local runtime evidence. This does not invalidate the existing unit-test results, which correctly label PostgreSQL as skipped.
- Minimal fix: add a separately named `compose-runtime` gate that executes the already authorized local `up`/readiness flow and retains its result, or explicitly mark this required gate NOT_RUN and keep full-release aggregation nonzero until an external/manual runtime result is supplied. Do not promote Compose syntax validation to a runtime PASS. Preserve existing volumes; do not add `down -v`.
- Present delivery treatment: **Compose runtime NOT_RUN**. No claim of fully validated local startup.

## What the source establishes

| Area | Code evidence | Source-review assessment | Runtime limit |
|---|---|---|---|
| M0 scope | `backend/app/main.py`: only `/api/health/live`, `/api/health/ready`, `/api/foundation`; public OpenAPI; no patient, encounter, order, login or mutation route | Consistent with C01/C05. Metadata explicitly reports clinical/authentication/role-access flags false. Role headers grant nothing. | Public route behavior has unit/outage-process evidence; no clinical APIs exist to test. |
| Deterministic fixture definition | `foundation/seed.py`: UUID5 namespace, fixed UTC timestamp and actor, fresh record dictionaries, seven exact role codes | Deterministic tenant + role + identity metadata only; no patient, citizen identifier, password or authenticated user fixture. | Actual PostgreSQL row persistence is NOT_RUN. |
| Seed idempotency and transaction | `seed_demo`: one `engine.begin()` across schema check, tenant/role/identity inserts and equality verification; `ON CONFLICT DO NOTHING` then exact expected-key/content lookup | Existing fixtures are verified, not overwritten. A conflicting primary/unique key or changed expected content raises inside the transaction. No `ON CONFLICT DO UPDATE`, truncation or deletion. | Transaction rollback/idempotent replay is established by source structure, not a completed live DB test. |
| Tenant/reference constraints | `models.py` and migration: nonnull tenant keys; composite `(tenant_id, role_code)` FK; RESTRICT deletes; unique fixture key per tenant | A demo identity cannot satisfy its role reference using a role belonging only to another tenant. Correctly does not claim row-level read isolation. | Constraint enforcement under PostgreSQL is NOT_RUN. |
| Non-login/synthetic flags | identity `login_enabled = false`, `synthetic_only = true` checks plus NOT NULL; tenant synthetic flag check | These flags constrain fixture declarations. They are not an authentication/RBAC system or semantic detector for real personal data. No public write route can populate arbitrary data. | PostgreSQL enforcement is NOT_RUN. |
| Migration shape | one revision creates tenant → role → identity; downgrade drops identity → role → tenant; UUID/timestamptz/check/FK definitions agree with models on inspection | Reversible structural foundation. Dropped tables are solely reproducible M0 metadata; there are no clinical records. | Offline SQL compilation PASS is narrower than live up/down/up PASS; the latter remains NOT_RUN. |
| Readiness | `database.py`: SELECT 1; exact Alembic revision; presence of each required public foundation table; unavailable/schema-pending paths; sanitized SQLAlchemy error | Reachable DB alone is not accepted. Liveness does not query the DB. DB connection/query timeouts are configured. No connection string returned/logged in the health failure path. | Actual ready=200 from the configured live database is NOT_RUN. A mock probe is not live readiness proof. |
| Configuration | `config.py`: explicit PostgreSQL+psycopg URL and local/test environment only, SecretStr, hidden/sanitized validation errors | No implicit SQLite/cloud service or OpenRouter key dependency. | URL validation alone does not prove network reachability. |
| Compose startup ordering | DB health → migrate success → seed success → backend health → frontend; published ports bind 127.0.0.1; persistent named volume | Dependency intent is coherent. Dockerfile uses nonroot app user; one-shot migration/seed failures block dependent startup. | Compose schema validation, image build and service execution are all NOT_RUN in this reviewer environment. |
| Local helper | `dev.py`: create-only `.env` with random hex DB secret, no shell subprocess, `up --build --detach --wait`, `down` without volume deletion, sanitized status display | Does not overwrite an existing secret file or destroy the DB volume. Generated hex secret avoids URL-special-character errors in the default Compose DSN. | Docker helper execution on a real workstation remains NOT_RUN. |
| Integration-test safety | test requires explicit `OMNIMED_TEST_DATABASE_URL`, database name `omnimed_test` or suffix, refuses existing public tables; no SQLite substitute | Appropriate opt-in disposable DB scope. The positive/negative integration scenario covers migration cycle, metadata drift, repeated seed, login check and tenant-role FK. | Entire integration test is SKIPPED in the supplied transcript. |

## Evidence actually available

Reviewed `validation/backend-build.txt` records:

- `uv lock --check` — EXIT 0.
- `uv sync --frozen --extra dev` — EXIT 0.
- Backend Ruff checks and formatting — PASS.
- Mypy — PASS for eight application source files.
- Backend pytest — **22 passed, 1 skipped**; the skipped item is the live PostgreSQL test.
- Offline PostgreSQL upgrade/downgrade SQL compilation — included in those unit tests, not a live migration.
- Real Uvicorn process smoke against an intentionally unavailable local PostgreSQL target: live endpoint 200, ready endpoint sanitized 503, foundation endpoint 200 with seven non-authenticated role previews.
- The transcript explicitly states this is the DB outage path only.

No tool or result in this second review executed Docker, built images, created a live database, applied a live migration, ran PostgreSQL seed persistence, or verified real DB constraints. Existing test execution was not repeated merely to duplicate a retained successful transcript.

## Follow-up required before an actual runtime PASS

Run the built Compose stack through the local helper, retain `/api/health/ready` 200 from the configured database, and run the existing disposable PostgreSQL integration test. Repair actual failures within the task loop budget. Until then retain the NOT_RUN entries and an incomplete runtime gate.

Earlier SG-001's missing `ai-agent-routing.zip` portion is resolved by root's later discovery and inspection, recorded in `docs/source/RECONCILIATION.md`; the previous review artifact remains a historical source-review snapshot, not the current claim about available inputs.
