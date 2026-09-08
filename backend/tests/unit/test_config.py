"""Explicit PostgreSQL URLs and acknowledged synthetic-demo settings only."""

import pytest

from app.config import ConfigurationError, load_settings


@pytest.mark.parametrize("environment", ["production", "prod", "staging", "", "LOCAL"])
def test_unexpected_environment_is_refused(environment: str) -> None:
    with pytest.raises(ConfigurationError) as error:
        load_settings({"APP_ENV": environment, "DATABASE_URL": "postgresql+psycopg://db/demo"})
    assert "APP_ENV" in str(error.value)


@pytest.mark.parametrize(
    "database_url",
    ["", "sqlite:///demo.db", "mysql://db/demo", "postgresql+psycopg:///demo", "bad-url"],
)
def test_non_postgres_or_implicit_database_is_refused(database_url: str) -> None:
    with pytest.raises(ConfigurationError):
        load_settings({"DATABASE_URL": database_url})


def test_configuration_failure_does_not_include_input_secrets() -> None:
    with pytest.raises(ConfigurationError) as error:
        load_settings(
            {
                "APP_ENV": "production",
                "DATABASE_URL": "postgresql+psycopg://local:private-sentinel@db/demo",
            }
        )
    assert "private-sentinel" not in str(error.value)
    assert "private-sentinel" not in repr(error.value)


def test_secret_repr_is_masked_and_optional_llm_key_is_unneeded() -> None:
    settings = load_settings(
        {"APP_ENV": "test", "DATABASE_URL": "postgresql+psycopg://local:private-sentinel@db/demo"}
    )
    assert settings.app_env == "test"
    assert settings.sqlalchemy_url.database == "demo"
    assert "private-sentinel" not in repr(settings)


@pytest.mark.parametrize("prefix", ["postgres", "postgresql", "postgresql+psycopg"])
def test_postgresql_urls_normalize_without_changing_connection_details(prefix: str) -> None:
    settings = load_settings(
        {
            "DATABASE_URL": (
                f"{prefix}://local:private%40sentinel@db:5433/omnimed_demo?sslmode=require"
            )
        }
    )
    url = settings.sqlalchemy_url
    assert url.drivername == "postgresql+psycopg"
    assert url.username == "local"
    assert url.password == "private@sentinel"
    assert url.host == "db"
    assert url.port == 5433
    assert url.database == "omnimed_demo"
    assert url.query["sslmode"] == "require"
    assert "private" not in repr(settings)


@pytest.mark.parametrize("acknowledgement", [None, "", "false", "1", "yes"])
def test_demo_environment_requires_explicit_synthetic_policy_acknowledgement(
    acknowledgement: str | None,
) -> None:
    environment = {"APP_ENV": "demo", "DATABASE_URL": "postgresql://db/omnimed_demo"}
    if acknowledgement is not None:
        environment["SYNTHETIC_DEMO_ONLY"] = acknowledgement
    with pytest.raises(ConfigurationError, match="SYNTHETIC_DEMO_ONLY=true"):
        load_settings(environment)


def test_demo_environment_accepts_explicit_synthetic_policy_acknowledgement() -> None:
    settings = load_settings(
        {
            "APP_ENV": "demo",
            "SYNTHETIC_DEMO_ONLY": "true",
            "DATABASE_URL": "postgres://db/omnimed_demo",
        }
    )
    assert settings.app_env == "demo"
    assert settings.synthetic_demo_only is True
