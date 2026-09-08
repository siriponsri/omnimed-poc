# OmniMed POC v0.1 — candidate delivery report

Date: 2026-09-08 · Scope: master M0 only + explicit user deployment amendment D01

**Release decision: BLOCKED_PENDING_RUNTIME_AND_FINAL_REVIEW.** ZIP is a concrete review/checkpoint candidate. Master §24 Definition of Done is not fully met because live Docker/PostgreSQL gates and final same-candidate independent reviews have not completed. Do not describe this package as fully validated, production-ready, full HIS or SRS-compliant

## What was implemented

- FastAPI/Pydantic/SQLAlchemy PostgreSQL foundation, versioned reversible Alembic migration and deterministic transactional seed of 1 synthetic tenant, 7 roles and 7 non-login identity fixtures
- Liveness/readiness/foundation endpoints, sanitized database failure, demo acknowledgement, PostgreSQL URL normalization and validated PORT launcher
- Next.js/TypeScript Thai-first shell with English, role-specific empty worklists, disabled future actions and server-side readiness status. Fonts bundled locally with OFL notice
- Authoritative local Docker Compose, nonroot app images, migrate/seed startup dependency chain, local helper, full disposable runtime gate and GitHub CI equivalent
- Optional Railway IaC + GitHub/dashboard deployment guide, environment variables, migration/start/seed commands, private service topology and health checks. No actual cloud resource or deployment
- Frozen contract, 53-module inventory, 153 exact requirement IDs, domain/security/event/FHIR documents, A01–A10 specifications, five ADRs, 23 task contracts/DAG, beginner learning guide and offline four-role control plane

## What actually ran

| Command / observation | Actual result | Retained evidence |
|---|---|---|
| uv sync --frozen --extra dev | Installed pinned environment | lockfiles; final checks use installed dependencies |
| python scripts/checks.py --full | Exit 1 because required Compose runtime NOT_RUN; all 9 executed entries PASS | local-checks/results.json and transcripts |
| backend_checks.py via runner | Ruff/format/mypy PASS; 43 tests passed, 1 live-PostgreSQL test skipped | local-checks/backend.txt |
| npm lint/typecheck/test/build in frontend | PASS; 2 unit tests; production build completed | local-checks/frontend-*.txt |
| pytest tests/tooling | 5 passed | local-checks/control-plane.txt |
| Real backend launcher in demo mode, unreachable local DB | live=200, foundation=200 with 7 roles/no access, ready=503 sanitized | backend-runtime-demo.txt |
| Standalone Compose config --quiet | Exit 0 (syntax only) | compose-config.txt |
| .railway npm run typecheck; npm test | Exit 0; 2 offline config evaluation tests passed | railway-config-check.txt |
| Manual browser on development preview | Role/locale/status interaction and desktop layout observed | browser-observations.md |
| Repository trace/task/package checks | Required files, 53 modules, 153 IDs, DAG and signature scan pass | local-checks/trace-and-package.txt; PACKAGE_MANIFEST.json |

No claim of Docker image startup, actual PostgreSQL migration/seed persistence, automated browser E2E, GitHub CI execution or Railway deployment is made. Those need an equipped host/account. No real PHI or external paid model API was used. Seed flags are declarations, not automated PHI classification

## Review and corrections

Historical SRS Guardian backend source PASS is retained with its original snapshot. Later focused delta review caught an over-strict health response assertion in the new full-runtime script; root fixed it. SG-B01 runtime-gate omission is fixed in source. Final independent reviews were interrupted by agent execution limits, so there is no dual-review signoff. See REVIEW_DISPOSITIONS for exact scope and limitations

Other repaired source/document issues include dev-preview hydration hostname, packaged public font notice/directory, exact finding-ID mapping, proposed Order interpretation labelling and current license metadata. Full test transcript includes non-failing dependency deprecation warnings; no clean security-scan claim is inferred

## Deliberately not implemented

M1–M5 clinical features, real login/RBAC, protected PHI access audit, patient data, CPOE/lab/dispense/billing/completion, FHIR endpoint/validator and OpenRouter network integration. Their schemas/APIs in docs are plans. A01–A10 are specifications, not passed scenarios. No IPD, clinical CDS, real stock, government/Next Account integration or production deployment

## Next work

1. On a Docker host, install dependencies/Chromium and run `python scripts/checks.py --full` under task M0-01. It builds an isolated test project; ordinary local startup remains `python scripts/dev.py up` and preserves data on down
2. Obtain current-candidate SRS Guardian and Reviewer verdicts and close runtime findings before declaring M0 release PASS
3. First clinical-domain task: **M1-01**, Party/Patient/identifier persistence and atomic HN allocation. It does not include registration UI or clinical HTTP endpoints
4. Before M3 revisions, accept ADR-0002 (SG-002). Before M5 completion, resolve signed note/principal diagnosis and synthetic account settlement in ADR-0004 (SG-003/004). No completion bypass is authorized

The downloadable ZIP excludes local secrets, environments, node_modules and build caches; keeps source/lockfiles/evidence. Original SRS/mockup binaries are not redistributed; exact review excerpts retain original rights. See README, HANDOFF_TO_CODEX and DEMO_DEPLOYMENT for commands
