"""Cross-platform deterministic backend gates; run with uv run python."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    "backend",
    "db",
    "scripts/backend_checks.py",
    "scripts/seed_demo.py",
    "scripts/start_backend.py",
]


def main() -> int:
    commands = [
        ["ruff", "check", *SOURCES],
        ["ruff", "format", "--check", *SOURCES],
        ["mypy"],
        ["pytest", "backend/tests", "-q"],
    ]
    for command in commands:
        print(f"+ python -m {' '.join(command)}", flush=True)
        result = subprocess.run([sys.executable, "-m", *command], cwd=ROOT, check=False)
        if result.returncode:
            return result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
