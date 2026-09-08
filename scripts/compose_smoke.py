"""Full local runtime gate in a new disposable Compose project.

Requires Docker Compose >=2.24.4, uv, Node and Playwright Chromium.
Only this script's random project and its test volume are removed. The ordinary
omnimed-poc project, .env and omnimed_data volume are never used or modified.
"""

from __future__ import annotations

import json
import os
import secrets
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def request(url: str, expected: int) -> object:
    try:
        with urllib.request.urlopen(url, timeout=15) as response:
            status, body = response.status, response.read().decode()
    except urllib.error.HTTPError as error:
        status, body = error.code, error.read().decode()
    if status != expected:
        raise RuntimeError(f"HTTP check failed: expected {expected}, got {status}")
    if "/api/" in url:
        return json.loads(body)
    if "OmniMed" not in body:
        raise RuntimeError("Frontend did not render the OmniMed page")
    return body


def main() -> int:
    docker, uv, npm = (shutil.which(name) for name in ("docker", "uv", "npm"))
    if not docker or not uv or not npm:
        print("NOT_RUN: Docker Compose, uv and Node.js are required.")
        return 2
    suffix = secrets.token_hex(6)
    project = f"omnimed-check-{suffix}"
    password = secrets.token_hex(24)
    env = dict(
        os.environ,
        POSTGRES_USER="omnimed",
        POSTGRES_PASSWORD=password,
        POSTGRES_DB="omnimed_demo",
        APP_ENV="local",
    )
    with tempfile.TemporaryDirectory(prefix="omnimed-check-") as temporary:
        temp = Path(temporary)
        (temp / "test.env").write_text("", encoding="utf-8")
        override = temp / "compose.check.yml"
        # Ephemeral loopback host ports avoid collisions with an owner's local stack.
        override.write_text(
            "services:\n"
            '  db:\n    ports: !override ["127.0.0.1::5432"]\n'
            '  backend:\n    ports: !override ["127.0.0.1::8000"]\n'
            '  frontend:\n    ports: !override ["127.0.0.1::3000"]\n',
            encoding="utf-8",
        )
        base = [
            docker,
            "compose",
            "--project-name",
            project,
            "--env-file",
            str(temp / "test.env"),
            "-f",
            str(ROOT / "docker-compose.yml"),
            "-f",
            str(override),
        ]

        def compose(*args: str, capture: bool = False) -> str:
            result = subprocess.run(
                [*base, *args],
                cwd=ROOT,
                env=env,
                text=True,
                stdout=subprocess.PIPE if capture else None,
                check=True,
            )
            return result.stdout.strip() if capture else ""

        def port(service: str, number: str) -> str:
            address = compose("port", service, number, capture=True)
            host, _, value = address.rpartition(":")
            if host != "127.0.0.1" or not value.isdigit():
                raise RuntimeError("Expected one ephemeral loopback port")
            return value

        try:
            compose("config", "--quiet")
            print("Building and starting disposable Compose project", flush=True)
            compose("up", "--build", "--detach", "--wait", "--wait-timeout", "240")
            api = "http://127.0.0.1:" + port("backend", "8000")
            web = "http://127.0.0.1:" + port("frontend", "3000")
            assert request(api + "/api/health/live", 200)["status"] == "alive"
            assert request(api + "/api/health/ready", 200)["status"] == "ready"
            request(api + "/api/foundation", 200)
            request(web, 200)
            assert request(web + "/api/status", 200) == {"status": "ready"}
            print("PASS: image build, startup ordering, live and database readiness", flush=True)

            # Real migration round-trip and seed constraints use a second, empty DB.
            test_db = f"omnimed_test_{suffix}"
            compose("exec", "-T", "db", "createdb", "-U", "omnimed", test_db)
            test_env = dict(
                env,
                OMNIMED_TEST_DATABASE_URL=f"postgresql+psycopg://omnimed:{password}@127.0.0.1:"
                f"{port('db', '5432')}/{test_db}",
            )
            result = subprocess.run(
                [uv, "run", "--frozen", "pytest", "backend/tests/integration", "-q"],
                cwd=ROOT,
                env=test_env,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            print(result.stdout.replace(password, "[REDACTED]"), end="")
            if result.returncode:
                raise RuntimeError("PostgreSQL integration gate failed")
            print("PASS: live PostgreSQL migration up/down/up, drift, seed and constraints")

            subprocess.run(
                [npm, "run", "test:e2e"],
                cwd=ROOT / "frontend",
                env=dict(env, OMNIMED_E2E_BASE_URL=web),
                check=True,
            )
            print("PASS: browser suite against built Compose frontend", flush=True)
            compose("stop", "db")
            request(api + "/api/health/live", 200)
            assert request(api + "/api/health/ready", 503)["status"] == "not_ready"
            assert request(web + "/api/status", 503) == {"status": "unavailable"}
            print("PASS: database outage gives live=200, ready/status=503")
            return 0
        except (
            subprocess.CalledProcessError,
            RuntimeError,
            AssertionError,
            OSError,
            ValueError,
        ) as error:
            # Avoid raw subprocess/driver diagnostics containing env-derived secrets.
            print(f"FAIL: Compose runtime gate ({type(error).__name__})", file=sys.stderr)
            return 1
        finally:
            # This explicit deletion is limited to the generated disposable project.
            subprocess.run(
                [*base, "down", "--volumes", "--remove-orphans"], cwd=ROOT, env=env, check=False
            )


if __name__ == "__main__":
    raise SystemExit(main())
