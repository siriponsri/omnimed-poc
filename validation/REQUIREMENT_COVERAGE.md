# Requirement coverage

Coverage here means trace coverage, not tested clinical implementation. Source inventory accounts for **53 modules**: 15 IN_SCOPE selected subsets, 12 DEFERRED, 26 OUT_OF_SCOPE. Counts derive from docs/source/module_inventory_53.csv

Selected trace has **153 unique exact SRS IDs** in **35 grouped rows** plus explicit-user M0/D01 rows. Each SRS entry retains body/table locator and verbatim excerpt in docs/source/selected_requirements.json. Source-review snapshots remain labelled proposed; root freeze/trace/ADRs state current disposition without rewriting source text

| Area | Current implementation | Evidence/limit |
|---|---|---|
| M0 runtime | FastAPI, Next, PostgreSQL config, migration, seed framework, health | Unit/build/native outage PASS; actual Compose/PG NOT_RUN |
| M0 UX | Seven-role Thai/EN shell, consistent empty worklists | Browser manual desktop observations; automated desktop/mobile/keyboard pending |
| M0 tenant metadata | Foundation tenant/role/non-login identities with constraints | Fixture/offline DDL tests; live enforcement pending |
| M0 control plane | Offline decision helper/fake provider/config/templates | Five tooling tests PASS; no live agent execution or paid API |
| M1–M5 domains | Documentation + 23 task DAG nodes including M0 verification | Patient/Encounter/Observation/Order/Charge/auth/audit/FHIR features NOT_IMPLEMENTED |
| A01–A10 | Written Given/When/Then and negatives | Clinical scenarios NOT_RUN / NOT_IMPLEMENTED |
| D01 Railway | Same Dockerfiles, env/PORT support, IaC, guide | SDK typecheck + two offline evaluation tests PASS; cloud plan/apply/deploy NOT_RUN |

Repository checker requires all 153 source IDs in the trace, all 53 modules, task files, acyclic known dependencies and required handoff paths. It does not prove SRS business-rule compliance or semantic PHI detection. No numeric percentage of full-HIS completion is claimed

Before each feature task, use its exact IDs/excerpts and update trace with new test paths/results. Keep SG-002 revision and SG-003/004 closure as BLOCKED_AMBIGUITY until explicit decisions. Do not upgrade planned SELECTED/PARTIAL_POC entries to implementation claims from this M0 report
