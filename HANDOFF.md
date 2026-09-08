# OmniMed M1-01 Handoff

This document is the authoritative handoff for the next session. It describes the current repository state as of 2026-09-09 and the remaining work required to close M1-01. Read `AGENTS.md` first; it is the project coding contract and takes precedence over this summary.

## Objective and scope

The active task is M1-01: Party / Patient / PatientIdentifier persistence. The intended implementation includes:

- Party identity with an explicit Party self relation.
- Patient persistence linked to Party.
- PatientIdentifier persistence with one preferred identifier per identifier type.
- Tenant-scoped composite foreign keys and uniqueness constraints.
- Atomic, concurrency-safe, never-reused generated HN values.
- Actor/time metadata on patient-domain tables.
- Versioned Alembic migration with explicit downgrade.
- Real PostgreSQL integration evidence for migration lifecycle and invariants.

The task explicitly excludes registration UI or HTTP registration, Encounter, Observation, Orders, medication/lab workflows, M2-M5 work, real PHI, external integrations, paid APIs, and LLMs in product runtime.

## Required reading order

Before changing code, read these files in this order:

1. `AGENTS.md`
2. `docs/POC_CONTRACT.md`
3. `.ai/TASK_TEMPLATE.md`
4. `docs/tasks/M1-01.md`
5. The exact M1-01 excerpts in `docs/source/SELECTED_SRS_EXCERPTS.md`
6. `docs/REQUIREMENT_TRACE.md`
7. `validation/FINAL_DELIVERY_REPORT.md`

For implementation, use the repository skills under `.agents/skills/`, especially `karpathy-guidelines`, `tdd`, `codebase-design`, `code-review`, and `omnimed-srs-guardian`. Guardian and Reviewer are read-only and must not edit product code.

## Repository and Git state

- Repository: `https://github.com/siriponsri/omnimed-poc`
- Branch: `feat/m1-01-patient-persistence`
- Latest pushed commit: `e4943ea` (`fix: correct patient metadata test`)
- Working tree was clean at the last code check. Gate runs rewrite files under `validation/local-checks/`; inspect those changes before committing them.
- Do not force-push and do not merge `main` automatically.

The repository did not contain `.git` when work began, so a new Git repository was initialized and the project was pushed to the requested branch. Preserve the existing branch and history; do not reset or discard user work.

## Implemented files and behavior

Relevant implementation files:

- `backend/app/patients/models.py`: `HnCounter`, `Party`, `PartyRelation`, `Patient`, and `PatientIdentifier` SQLAlchemy models.
- `backend/app/patients/service.py`: `allocate_hn(session, tenant_id, actor, prefix="HN")`, using a PostgreSQL upsert and row lock inside the caller's transaction.
- `backend/app/patients/__init__.py`: patient model exports.
- `db/migrations/versions/0002_patient_persistence.py`: Party/patient schema, named constraints, preferred identifier partial unique index, upgrade and downgrade.
- `db/migrations/env.py`: imports patient models so Alembic metadata includes them.
- `backend/app/database.py`: readiness expects revision `0002_patient_persistence` and patient-domain tables.
- `backend/tests/unit/test_patient_persistence.py`: metadata-level invariant checks.
- `backend/tests/integration/test_postgresql.py`: existing disposable PostgreSQL migration/seed/drift checks.
- `docs/assets/omnimed-logo.svg`: original restrained logo.

Important schema details:

- Patient-to-Party and identifier-to-Patient references use composite `(tenant_id, id)` keys, preventing cross-tenant links at the database boundary.
- `party_relation` has separately named FKs: `fk_party_relation_party` and `fk_party_relation_related_party`.
- Patient uniqueness is named and tenant-scoped: HN, Party link, and patient identity.
- `uq_patient_identifier_preferred` is a PostgreSQL partial unique index on `(tenant_id, patient_id, identifier_type)` where `is_preferred` is true.
- Audit columns are `created_at`, `created_by`, `updated_at`, and `updated_by`.
- No patient HTTP endpoint or clinical hard-delete path was added.

## Verified evidence

The latest successful full gate was run after fixing duplicate PostgreSQL constraint names and SQLAlchemy/Alembic metadata drift. The retained transcript reports:

- `uv run python scripts/backend_checks.py`: PASS.
- `uv run python scripts/checks.py`: PASS.
- `uv run python scripts/checks.py --full`: PASS.
- Backend lint, formatting, strict mypy, frontend lint/typecheck/unit/build: PASS.
- Live PostgreSQL migration upgrade → downgrade → upgrade: PASS.
- PostgreSQL schema drift check: PASS.
- Seed and constraint checks: PASS.
- Compose browser suite: PASS.
- Database outage behavior: PASS (`live=200`, readiness/status `503`).
- Backend test count at that point: `43 passed, 1 skipped`; after adding the metadata test, the expected count is `44 passed, 1 skipped`, but rerun the full gate on the current commit before reporting a final count.

Evidence is in `validation/local-checks/compose-runtime-postgres-browser.txt` and related files. Never convert `SKIP`, `NOT_RUN`, or unavailable evidence into PASS.

## Remaining work before completion

The previous review deliberately did not claim full Definition of Done. The next session should complete these items:

1. Add meaningful PostgreSQL integration tests, guarded by the existing disposable database contract, for:
   - concurrent HN allocation from multiple transactions/threads, asserting no duplicate HNs;
   - HN non-reuse after an allocated patient/row is removed or a transaction is rolled back, according to the exact task semantics;
   - duplicate preferred identifiers of the same type being rejected;
   - two preferred identifiers of different types being allowed;
   - cross-tenant Party→Patient, PartyRelation, and PatientIdentifier references being rejected by PostgreSQL;
   - actor/time metadata being persisted.
2. Confirm the HN service transaction contract. `allocate_hn` must be called inside the caller's transaction; document this explicitly and ensure failed patient creation cannot consume a number unless the task's non-reuse rule requires allocation to be monotonic despite failure.
3. Update `docs/REQUIREMENT_TRACE.md`, `docs/DOMAIN_MODEL.md`, `docs/tasks/M1-01.md`, and `validation/FINAL_DELIVERY_REPORT.md` with exact requirement IDs, test names, commands, exit codes, candidate SHA, and limitations. Keep future work marked `NOT_IMPLEMENTED`.
4. Update `README.md` with accurate synthetic-only/non-production status, implemented versus planned features, architecture, stack, setup, validation, project structure, security boundaries, agent workflow, and roadmap. Do not claim regulatory compliance, fake test totals, deployment URLs, or unimplemented features.
5. Run all required commands on the same candidate:

   ```text
   uv sync --frozen --extra dev
   uv run python scripts/backend_checks.py
   uv run python scripts/checks.py
   uv run python scripts/checks.py --full
   ```

6. Run the read-only SRS Guardian after deterministic gates. It must return exactly one of `PASS`, `FAIL`, or `UNCERTAIN`, with SRS citations and evidence. A passing runtime gate alone is not SRS compliance.
7. Run the read-only Reviewer after Guardian. Record standards/security/spec findings and verdict for the same candidate. Do not edit product code from either review.
8. Perform a final git status/remote check, commit only related changes, push without force, and report the final SHA and branch.

## Known limitations and non-goals

- No registration UI or patient HTTP registration flow.
- No authenticated protected patient routes, production IAM, RLS, encryption, or PHI.
- No Encounter, Observation, Order, medication, laboratory, charge, finance, FHIR, or external integration implementation.
- No citizen-ID fixtures; synthetic identifiers only.
- No production deployment or cloud provisioning.
- `HnCounter` and allocation service are persistence/domain primitives, not a registration workflow.

## Suggested next-session procedure

1. Inspect `git status`, branch, remote, and latest commit. Do not reset the branch.
2. Re-read the required documents above and inspect the current patient models, migration, service, and tests.
3. Implement the PostgreSQL integration tests first (TDD), preserving the disposable empty `omnimed_test[_suffix]` database requirement.
4. Fix only defects exposed by those tests. Avoid broad M0 refactors.
5. Run the deterministic gates and inspect every result, including exit codes and retained transcripts.
6. Update the four required documentation/evidence files and README with facts from the current candidate.
7. Run SRS Guardian and Reviewer as read-only reviews. Address material findings within the repair-loop limits in `AGENTS.md`.
8. Commit and push the final candidate, then produce the requested ten-item handoff report.

## Final report checklist

The final response must list:

1. changed files;
2. migrations added;
3. tests added;
4. exact requirement IDs satisfied;
5. deterministic gate results;
6. SRS Guardian verdict;
7. Reviewer verdict;
8. remaining limitations / `NOT_IMPLEMENTED` items;
9. commit SHA;
10. pushed branch and repository status.

Do not mark M1-01 complete until every required item has direct evidence from the same candidate.
