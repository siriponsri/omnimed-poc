# Run record template

Task / start+finish UTC / assigned four roles:
Candidate digest: `python scripts/repository_check.py --digest`
Dependencies / accepted ADRs:
Builder changed files:
Gate commands, exit codes and transcript paths:
Guardian PASS/FAIL/UNCERTAIN, same digest, non-mock source, evidence:
Reviewer PASS/FAIL/UNCERTAIN, same digest, non-mock source, evidence:
Findings / repairs used / max budget:
Decision PASS/FIX/REROUTE/BLOCKED_REQUIRES_HUMAN:
API usage/cost (default zero) / provider failures:
Limitations / next task:

Machine input shape: .ai/examples/incomplete-run.json. Reviews contain verdict/candidate_sha256/evidence/source. repairs_used counts previous rounds; hard_blocker/scope_blocked/reroute เป็น boolean. ห้ามเขียน secrets. Source เปลี่ยนทำให้ review digest เก่าใช้ไม่ได้
