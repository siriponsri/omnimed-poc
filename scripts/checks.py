"""Local CI equivalent; optional gates cannot be reported as PASS when omitted."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--full",
        action="store_true",
        help="Build an isolated Compose stack; require real PostgreSQL and browser gates.",
    )
    args = parser.parse_args()
    uv = shutil.which("uv")
    npm = shutil.which("npm")
    if not uv or not npm:
        print(
            "Install uv and Node.js; run uv sync --frozen --extra dev and npm ci in frontend first."
        )
        return 2
    gates: list[tuple[str, list[str] | None, Path]] = [
        ("backend", [uv, "run", "--frozen", "python", "scripts/backend_checks.py"], ROOT),
        ("frontend-lint", [npm, "run", "lint"], ROOT / "frontend"),
        ("frontend-typecheck", [npm, "run", "typecheck"], ROOT / "frontend"),
        ("frontend-unit", [npm, "test"], ROOT / "frontend"),
        ("frontend-build", [npm, "run", "build"], ROOT / "frontend"),
        ("control-plane", [uv, "run", "--frozen", "pytest", "tests/tooling", "-q"], ROOT),
        (
            "tooling-lint",
            [uv, "run", "--frozen", "ruff", "check", "scripts", "tests/tooling"],
            ROOT,
        ),
        (
            "tooling-format",
            [uv, "run", "--frozen", "ruff", "format", "--check", "scripts", "tests/tooling"],
            ROOT,
        ),
        ("trace-and-package", [sys.executable, "scripts/repository_check.py"], ROOT),
        (
            "compose-runtime-postgres-browser",
            [sys.executable, "scripts/compose_smoke.py"]
            if args.full and shutil.which("docker")
            else None,
            ROOT,
        ),
    ]
    evidence = ROOT / "validation/local-checks"
    evidence.mkdir(parents=True, exist_ok=True)
    results = []
    failed = False
    env = dict(os.environ, NEXT_TELEMETRY_DISABLED="1", UV_NO_SYNC="1")
    for name, command, cwd in gates:
        if command is None:
            state = "NOT_RUN"
            results.append(
                {
                    "gate": name,
                    "status": state,
                    "reason": "Full gate not selected or Docker executable unavailable",
                }
            )
            failed |= args.full
            print(f"{name}: {state}")
            continue
        start = time.monotonic()
        # No shell; every command is repository-owned and secrets are never part of argv.
        result = subprocess.run(
            command,
            cwd=cwd,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="utf-8",
            errors="replace",
        )
        content = result.stdout
        for key in [
            "OPENROUTER_API_KEY",
            "DATABASE_URL",
            "OMNIMED_TEST_DATABASE_URL",
            "POSTGRES_PASSWORD",
        ]:
            if env.get(key):
                content = content.replace(env[key], "[REDACTED]")
        (evidence / f"{name}.txt").write_text(content, encoding="utf-8")
        state = "PASS" if result.returncode == 0 else "FAIL"
        results.append(
            {
                "gate": name,
                "status": state,
                "command": command,
                "exit_code": result.returncode,
                "seconds": round(time.monotonic() - start, 2),
                "evidence": f"validation/local-checks/{name}.txt",
            }
        )
        failed |= result.returncode != 0
        print(f"{name}: {state}", flush=True)
    (evidence / "results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print("Full release gate requires all entries PASS; NOT_RUN is never a pass.")
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
