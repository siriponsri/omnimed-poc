"""Public runtime behavior and negative boundary tests without a database substitute."""

from fastapi.testclient import TestClient
from sqlalchemy import Engine
from sqlalchemy.exc import OperationalError

from app.database import Readiness, check_readiness
from app.main import create_app


def test_liveness_does_not_query_database() -> None:
    def unused_probe() -> Readiness:
        raise AssertionError("Liveness must not depend on database availability")

    with TestClient(create_app(readiness_probe=unused_probe)) as client:
        response = client.get("/api/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "alive", "service": "omnimed-api"}
    assert response.headers["cache-control"] == "no-store"
    assert response.headers["x-content-type-options"] == "nosniff"


def test_database_outage_returns_sanitized_503() -> None:
    class FailingEngine:
        def connect(self) -> None:
            raise OperationalError(
                "SELECT 1", {}, RuntimeError("private-connection-sentinel database unavailable")
            )

    def probe() -> Readiness:
        return check_readiness(FailingEngine())  # type: ignore[arg-type]

    with TestClient(create_app(readiness_probe=probe)) as client:
        response = client.get("/api/health/ready")
    assert response.status_code == 503
    assert response.json() == {
        "status": "not_ready",
        "database": "unavailable",
        "schema": "unknown",
    }
    assert "private-connection-sentinel" not in response.text


def test_reachable_database_with_pending_schema_is_not_ready() -> None:
    state = Readiness(status="not_ready", database="reachable", schema="pending")
    with TestClient(create_app(readiness_probe=lambda: state)) as client:
        response = client.get("/api/health/ready")
    assert response.status_code == 503
    assert response.json()["schema"] == "pending"


def test_current_schema_reports_ready() -> None:
    state = Readiness(status="ready", database="reachable", schema="current")
    with TestClient(create_app(readiness_probe=lambda: state)) as client:
        response = client.get("/api/health/ready")
    assert response.status_code == 200
    assert response.json() == state.model_dump(by_alias=True)


def test_role_preview_never_grants_clinical_access() -> None:
    state = Readiness(status="ready", database="reachable", schema="current")
    with TestClient(create_app(readiness_probe=lambda: state)) as client:
        metadata = client.get("/api/foundation", headers={"X-Role": "R-ADMIN"}).json()
        for role in ("R-REG", "R-DOC", "R-FIN", "R-ADMIN"):
            for path in ("/api/patients", "/api/encounters", "/api/orders", "/api/login"):
                response = client.get(path, headers={"X-Role": role})
                assert response.status_code == 404
    assert metadata["authentication_available"] is False
    assert metadata["clinical_features_available"] is False
    assert metadata["role_preview_grants_access"] is False
    assert {role["code"] for role in metadata["roles"]} == {
        "R-REG",
        "R-SCR",
        "R-DOC",
        "R-LAB",
        "R-PHA",
        "R-FIN",
        "R-ADMIN",
    }


def test_public_schema_has_only_foundation_routes_and_no_cdn_docs() -> None:
    state = Readiness(status="ready", database="reachable", schema="current")
    with TestClient(create_app(readiness_probe=lambda: state)) as client:
        schema = client.get("/openapi.json").json()
        assert client.get("/docs").status_code == 404
        assert client.get("/redoc").status_code == 404
    assert set(schema["paths"]) == {"/api/health/live", "/api/health/ready", "/api/foundation"}


def test_readiness_queries_schema_presence_and_exact_revision() -> None:
    from unittest.mock import MagicMock

    from app.database import EXPECTED_REVISION

    engine = MagicMock(spec=Engine)
    connection = engine.connect.return_value.__enter__.return_value
    connection.scalar.return_value = None
    assert check_readiness(engine).schema_status == "pending"

    connection.scalar.return_value = "alembic_version"
    connection.scalars.return_value.all.return_value = ["unrecognized-revision"]
    assert check_readiness(engine).schema_status == "pending"

    connection.scalars.return_value.all.return_value = [EXPECTED_REVISION]
    connection.scalar.side_effect = ["alembic_version", "foundation_tenant", None]
    assert check_readiness(engine).schema_status == "pending"

    connection.scalar.side_effect = None
    connection.scalar.return_value = "present"
    assert check_readiness(engine).status == "ready"
