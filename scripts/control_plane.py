"""Offline decision interface for four-role task reviews. Does not execute agents."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Protocol

Verdict = Literal["PASS", "FAIL", "UNCERTAIN"]
Decision = Literal["PASS", "FIX", "REROUTE", "BLOCKED_REQUIRES_HUMAN"]


@dataclass(frozen=True)
class Review:
    verdict: Verdict
    candidate_sha256: str
    evidence: str
    source: Literal["human", "agent", "mock"]


class ReviewProvider(Protocol):
    def review(self, task_id: str, candidate_sha256: str) -> Review: ...


class FakeProvider:
    """Test double only. Mock review cannot satisfy a delivery decision."""

    def review(self, task_id: str, candidate_sha256: str) -> Review:
        return Review("UNCERTAIN", candidate_sha256, f"offline-fixture:{task_id}", "mock")


def decide(
    *,
    candidate_sha256: str,
    gates: dict[str, str],
    guardian: Review,
    reviewer: Review,
    repairs_used: int = 0,
    hard_blocker: bool = False,
    scope_blocked: bool = False,
    reroute: bool = False,
) -> Decision:
    if (
        not isinstance(candidate_sha256, str)
        or len(candidate_sha256) != 64
        or any(c not in "0123456789abcdef" for c in candidate_sha256)
        or type(repairs_used) is not int
        or not 0 <= repairs_used <= 3
    ):
        raise ValueError("Invalid candidate digest or repair counter")
    if (
        not isinstance(gates, dict)
        or any(
            not isinstance(k, str) or v not in {"PASS", "FAIL", "NOT_RUN", "SKIP"}
            for k, v in gates.items()
        )
        or any(type(flag) is not bool for flag in (hard_blocker, scope_blocked, reroute))
        or any(
            not isinstance(r, Review)
            or not isinstance(r.evidence, str)
            or r.verdict not in {"PASS", "FAIL", "UNCERTAIN"}
            or r.source not in {"human", "agent", "mock"}
            for r in (guardian, reviewer)
        )
    ):
        raise ValueError("Invalid gates or review record")
    budget = 3 if hard_blocker else 2
    if scope_blocked or repairs_used > budget:
        return "BLOCKED_REQUIRES_HUMAN"
    required = {"test", "lint", "typecheck", "build", "migration"}
    valid_reviews = all(
        r.verdict == "PASS"
        and r.candidate_sha256 == candidate_sha256
        and bool(r.evidence.strip())
        and r.source in {"human", "agent"}
        for r in [guardian, reviewer]
    )
    if required <= gates.keys() and all(v == "PASS" for v in gates.values()) and valid_reviews:
        return "PASS"
    if repairs_used >= budget:
        return "BLOCKED_REQUIRES_HUMAN"
    return "REROUTE" if reroute else "FIX"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.record.read_text(encoding="utf-8"))
        data["guardian"] = Review(**data["guardian"])
        data["reviewer"] = Review(**data["reviewer"])
        print(json.dumps({"decision": decide(**data), "mode": "offline-record-evaluation"}))
        return 0
    except (TypeError, ValueError, KeyError, OSError):
        print(json.dumps({"decision": "BLOCKED_REQUIRES_HUMAN", "reason": "Invalid run record"}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
