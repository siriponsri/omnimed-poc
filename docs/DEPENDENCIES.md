# Dependency and provenance snapshot

ตรวจจาก installed package metadata/lockfiles เมื่อ 2026-09-08. เป็น direct dependency inventory ไม่ใช่ full transitive vulnerability audit หรือ legal clearance. Images/OS packages มี license ของตนเอง. เก็บ uv.lock และ npm lockfiles; framework updates ต้อง rerun gates

| Area | Package | Version | Declared license / metadata |
|---|---|---|---|
| Backend runtime | alembic | 1.19.2 | MIT |
| Backend runtime | fastapi | 0.141.1 | MIT |
| Backend runtime | pydantic | 2.13.5 | MIT |
| Backend runtime | psycopg | 3.3.5 | LGPL-3.0-only |
| Backend runtime | sqlalchemy | 2.0.52 | MIT |
| Backend runtime | uvicorn | 0.52.4 | BSD-3-Clause |
| Backend dev | httpx | 0.28.1 | BSD-3-Clause |
| Backend dev | mypy | 2.3.1 | MIT |
| Backend dev | pytest | 9.1.1 | MIT |
| Backend dev | ruff | 0.16.6 | MIT |
| Frontend dependencies | @fontsource/sarabun | 5.2.8 | OFL-1.1 |
| Frontend dependencies | next | 16.3.4 | MIT |
| Frontend dependencies | react | 19.2.8 | MIT |
| Frontend dependencies | react-dom | 19.2.8 | MIT |
| Frontend devDependencies | @playwright/test | 1.58.2 | Apache-2.0 |
| Frontend devDependencies | @types/node | 22.19.15 | MIT |
| Frontend devDependencies | @types/react | 19.2.14 | MIT |
| Frontend devDependencies | @types/react-dom | 19.2.3 | MIT |
| Frontend devDependencies | eslint | 9.39.4 | MIT |
| Frontend devDependencies | eslint-config-next | 16.3.4 | MIT |
| Frontend devDependencies | typescript | 5.9.3 | Apache-2.0 |
| Railway tooling dependencies | railway | 3.11.0 | MIT |
| Railway tooling devDependencies | typescript | 5.9.3 | Apache-2.0 |
| Railway tooling devDependencies | @types/node | 22.19.15 | MIT |

Python image: python:3.12.13-slim-bookworm; uv builder binary: 0.11.33; Node image: node:24.20.0-bookworm-slim; local database: postgres:17.11-bookworm. Railway SDK helper selects its Postgres 18 template, which must be validated separately on demo deployment. No product import of Railway, OpenRouter, Agents SDK, CrewAI or OpenHands

Sarabun font is bundled locally via @fontsource/sarabun (OFL-1.1); no Google Fonts/CDN runtime request. Framework library license notices remain in installed package distributions. No copied application code/assets from reference repos. Uploaded source excerpts retain their original rights; see LICENSE_NOTE.md and REFERENCE_AUDIT.md

Known test-only warnings: FastAPI/Starlette TestClient deprecates httpx integration and an anyio alias. Current assertions pass; review tooling compatibility during dependency updates. No claim that a passing build proves absence of vulnerabilities
