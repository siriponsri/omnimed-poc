"""Local/test runtime and explicitly acknowledged synthetic demo configuration."""

import os
from collections.abc import Mapping
from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    SecretStr,
    ValidationError,
    field_validator,
    model_validator,
)
from sqlalchemy.engine import URL, make_url
from sqlalchemy.exc import ArgumentError


class ConfigurationError(RuntimeError):
    """A deliberately sanitized configuration failure."""


class Settings(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", hide_input_in_errors=True)

    app_env: Literal["local", "test", "demo"] = "local"
    database_url: SecretStr
    synthetic_demo_only: bool = False

    @field_validator("database_url")
    @classmethod
    def postgres_only(cls, value: SecretStr) -> SecretStr:
        try:
            url = make_url(value.get_secret_value())
            valid = (
                url.drivername in {"postgres", "postgresql", "postgresql+psycopg"}
                and bool(url.host)
                and bool(url.database)
            )
        except (ArgumentError, ValueError):
            valid = False
        if not valid:
            raise ValueError(
                "DATABASE_URL must be an explicit PostgreSQL URL with host and database"
            )
        return SecretStr(
            url.set(drivername="postgresql+psycopg").render_as_string(hide_password=False)
        )

    @model_validator(mode="after")
    def acknowledge_synthetic_demo(self) -> "Settings":
        # This policy flag is an operator acknowledgement, not a PHI detection mechanism.
        if self.app_env == "demo" and not self.synthetic_demo_only:
            raise ValueError("APP_ENV=demo requires SYNTHETIC_DEMO_ONLY=true")
        return self

    @property
    def sqlalchemy_url(self) -> URL:
        return make_url(self.database_url.get_secret_value())


def load_settings(environ: Mapping[str, str] | None = None) -> Settings:
    source = os.environ if environ is None else environ
    try:
        return Settings(
            app_env=source.get("APP_ENV", "local"),  # type: ignore[arg-type]
            database_url=SecretStr(source.get("DATABASE_URL", "")),
            synthetic_demo_only=source.get("SYNTHETIC_DEMO_ONLY") == "true",
        )
    except ValidationError:
        raise ConfigurationError(
            "Invalid configuration: APP_ENV must be local, test or demo; "
            "demo requires SYNTHETIC_DEMO_ONLY=true; "
            "DATABASE_URL must be an explicit PostgreSQL URL."
        ) from None
