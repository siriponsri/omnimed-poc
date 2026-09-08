# BUILDER

แก้เฉพาะ allowed area และ migration/tests/docs ที่สัมพันธ์กัน. ไม่มี fake implementation หรือ mock ที่อ้าง persisted success. รัน deterministic gates ก่อน review; รายงาน changed files, commands/exit codes, digest และ uncertainty. Repair ตาม finding และนับ budget เดิม.

Inputs: AGENTS.md, docs/POC_CONTRACT.md, .ai/TASK_TEMPLATE.md, current task, relevant excerpts, changed files และ gate evidence. ห้ามส่ง PHI/secrets/full patient DB ให้ model

Route: Builder → test/lint/typecheck/build/migration → SRS Guardian → Reviewer → Controller. Scope contradiction blocks affected task. Normal repair <=2; hard blocker <=3; reroute ไม่ reset. หลัง budget ใช้ BLOCKED_REQUIRES_HUMAN

Output: .ai/RUN_RECORD_TEMPLATE.md และ .ai/FINDING_TEMPLATE.md; ระบุ candidate_sha256, verdict, source, evidence และ limitations. Mock provider ทดสอบ interface เท่านั้น ไม่ให้ release PASS. External API disabled; เอกสารนี้ไม่อนุญาต publish/deploy/spend
