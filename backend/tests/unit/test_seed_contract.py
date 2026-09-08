"""Fixture construction tests; PostgreSQL persistence is tested separately."""

from app.foundation.seed import fixture_records


def test_fixture_records_are_deterministic_synthetic_and_have_no_credentials() -> None:
    first = fixture_records()
    second = fixture_records()
    assert first == second
    tenant, roles, identities = first
    assert tenant["synthetic_only"] is True
    assert len(roles) == len(identities) == 7
    assert len({identity["id"] for identity in identities}) == 7
    assert len({identity["fixture_key"] for identity in identities}) == 7
    assert {identity["role_code"] for identity in identities} == {role["code"] for role in roles}
    for identity in identities:
        assert identity["synthetic_only"] is True
        assert identity["login_enabled"] is False
        assert identity["tenant_id"] == tenant["id"]
        assert not ({"password", "password_hash", "citizen_id", "patient_id"} & identity.keys())
        assert identity["created_by"] == identity["updated_by"] == "system:m0-fixture-v1"
        assert identity["created_at"] == identity["updated_at"]


def test_mutating_a_fixture_result_does_not_change_future_seed_content() -> None:
    _, _, identities = fixture_records()
    identities[0]["display_name"] = "mutated"
    assert fixture_records()[2][0]["display_name"] != "mutated"
