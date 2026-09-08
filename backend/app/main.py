"""Only public, non-PHI endpoints exist in M0; no role header enables access."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
from sqlalchemy import Engine
from starlette.middleware.base import RequestResponseEndpoint

from app import __version__
from app.config import Settings, load_settings
from app.database import Probe, Readiness, build_engine, check_readiness
from app.foundation.catalog import ROLES, RolePreview


class Liveness(BaseModel):
    status: Literal["alive"] = "alive"
    service: Literal["omnimed-api"] = "omnimed-api"


class FoundationMetadata(BaseModel):
    milestone: Literal["M0"] = "M0"
    version: str = __version__
    synthetic_only: bool = True
    clinical_features_available: bool = False
    authentication_available: bool = False
    role_preview_grants_access: bool = False
    roles: tuple[RolePreview, ...] = ROLES


def create_app(settings: Settings | None = None, readiness_probe: Probe | None = None) -> FastAPI:
    engine: Engine | None = None
    if readiness_probe is None:
        engine = build_engine(settings or load_settings())

        def probe() -> Readiness:
            assert engine is not None
            return check_readiness(engine)

        readiness_probe = probe

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        try:
            yield
        finally:
            if engine is not None:
                engine.dispose()

    api = FastAPI(
        title="OmniMed M0 Foundation API",
        version=__version__,
        description="Public non-PHI health and role-preview metadata. Clinical APIs are deferred.",
        docs_url=None,
        redoc_url=None,
        openapi_url="/openapi.json",
        lifespan=lifespan,
        debug=False,
    )

    @api.middleware("http")
    async def response_headers(request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        return response

    @api.get("/api/health/live", response_model=Liveness, tags=["health"])
    def live() -> Liveness:
        return Liveness()

    @api.get(
        "/api/health/ready",
        response_model=Readiness,
        responses={503: {"model": Readiness, "description": "Database or schema is not ready"}},
        tags=["health"],
    )
    def ready(response: Response) -> Readiness:
        assert readiness_probe is not None
        result = readiness_probe()
        if result.status != "ready":
            response.status_code = 503
        return result

    @api.get("/api/foundation", response_model=FoundationMetadata, tags=["foundation"])
    def foundation() -> FoundationMetadata:
        return FoundationMetadata()

    return api
