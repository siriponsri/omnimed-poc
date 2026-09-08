from scripts.control_plane import FakeProvider, Review, decide

SHA = "a" * 64


def record():
    return dict(
        candidate_sha256=SHA,
        gates={k: "PASS" for k in ["test", "lint", "typecheck", "build", "migration"]},
        guardian=Review("PASS", SHA, "guardian.md", "agent"),
        reviewer=Review("PASS", SHA, "reviewer.md", "human"),
    )


def test_complete_matching_evidence_can_pass():
    assert decide(**record()) == "PASS"


def test_skip_stale_review_and_mock_cannot_pass():
    r = record()
    r["gates"]["migration"] = "NOT_RUN"
    assert decide(**r) == "FIX"
    r = record()
    r["reviewer"] = Review("PASS", "b" * 64, "old.md", "human")
    assert decide(**r) == "FIX"
    r = record()
    r["guardian"] = FakeProvider().review("M1-01", SHA)
    assert decide(**r) == "FIX"


def test_budget_and_scope_cannot_be_bypassed_by_rerouting():
    r = record()
    r["gates"]["test"] = "FAIL"
    assert decide(**r, repairs_used=2, reroute=True) == "BLOCKED_REQUIRES_HUMAN"
    assert decide(**r, repairs_used=2, hard_blocker=True) == "FIX"
    assert decide(**r, repairs_used=3, hard_blocker=True) == "BLOCKED_REQUIRES_HUMAN"
    assert decide(**record(), scope_blocked=True) == "BLOCKED_REQUIRES_HUMAN"


def test_a_complete_record_cannot_exceed_the_normal_repair_budget():
    assert decide(**record(), repairs_used=3) == "BLOCKED_REQUIRES_HUMAN"


def test_malformed_inputs_fail_closed():
    import pytest

    with pytest.raises(ValueError):
        decide(**record(), repairs_used=True)
    broken = record()
    broken["candidate_sha256"] = None
    with pytest.raises(ValueError):
        decide(**broken)
    broken = record()
    broken["gates"] = []
    with pytest.raises(ValueError):
        decide(**broken)
