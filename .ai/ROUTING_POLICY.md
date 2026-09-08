# Routing and cost policy

Manual stage-gated interface สำหรับ Codex/OpenRouter ในอนาคต. `scripts/control_plane.py` ประเมิน record เท่านั้น ไม่ execute agents ไม่รัน prompt เป็น shell และไม่มี network provider

| Role | Class | Context | Writes |
|---|---|---|---|
| Orchestrator | high_reasoning | contract/task/findings | task/docs; explicit Builder takeover if necessary |
| Builder | coding | scoped files/excerpts | implementation |
| SRS Guardian | low_cost_reasoning | source/diff/gates | no product writes |
| Reviewer | medium_reasoning | diff/tests/UX/license | no product writes |

2 normal repair loops / 3 hard blockers; counters อยู่กับ task แม้เปลี่ยน model. Provider error ไม่เป็น PASS. Scope ambiguity ให้ BLOCKED_REQUIRES_HUMAN; environment missing ให้ NOT_RUN พร้อม next command

`routing.example.yaml` เป็น config example ไม่ใช่ executable scheduler/YAML loader. Future OpenRouter อ่าน OPENROUTER_API_KEY จาก env เมื่อ opt-in implementation เท่านั้น. ปัจจุบัน allow_network=false, allowed models=[], live budget USD 0. Model names อยู่ tooling config; future provider ต้องมี timeout/token/cost cap, explicit fallback, no secret logging และ offline FakeProvider tests

PASS ต้องมี test/lint/typecheck/build/migration และ supplied extra gates ทั้งหมด PASS; Guardian/Reviewer PASS, non-mock และ digest เดียวกัน. Helper ไม่ตรวจเนื้อหา/ลายเซ็น evidence file: trusted operator ยังต้องตรวจ transcript จริง. ไม่ใช่ tamper-proof attestation

```sh
python scripts/control_plane.py .ai/examples/incomplete-run.json
```

Expected FIX เพราะ mock review UNCERTAIN. อย่าใช้ตัวอย่างนี้เป็นหลักฐานว่างานจริงผ่าน. REROUTE ไม่ reset budget; scope block ชนะ verdict อื่น
