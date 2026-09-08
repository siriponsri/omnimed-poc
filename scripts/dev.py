"""Cross-platform local Compose commands. Never removes database volumes."""

from __future__ import annotations

import argparse
import os
import secrets
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def initialize() -> None:
    target = ROOT / ".env"
    if target.exists():
        print(".env already exists; kept unchanged.")
        return
    text = (ROOT / ".env.example").read_text(encoding="utf-8")
    text = text.replace("POSTGRES_PASSWORD=\n", f"POSTGRES_PASSWORD={secrets.token_hex(24)}\n")
    # O_EXCL prevents clobbering an existing secret file in a concurrent run.
    fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as output:
        output.write(text)
    print("Created .env with a generated local database password.")


def compose(*args: str) -> int:
    docker = shutil.which("docker")
    if docker is None:
        print("Docker Compose v2 is required. Open Docker Desktop, then retry.", file=sys.stderr)
        return 2
    return subprocess.call([docker, "compose", *args], cwd=ROOT)


def status() -> int:
    failed = False
    for label, url in [
        ("frontend", "http://127.0.0.1:3000"),
        ("backend live", "http://127.0.0.1:8000/api/health/live"),
        ("backend ready", "http://127.0.0.1:8000/api/health/ready"),
    ]:
        try:
            with urllib.request.urlopen(url, timeout=8) as response:
                print(f"{label}: HTTP {response.status}")
        except (urllib.error.URLError, TimeoutError):
            print(f"{label}: unavailable")
            failed = True
    return int(failed)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["init", "up", "down", "config", "status", "logs"])
    args = parser.parse_args()
    if args.action == "init":
        initialize()
        return 0
    if args.action == "status":
        return status()
    if args.action == "up":
        initialize()
        result = compose("config", "--quiet")
        if result:
            return result
        result = compose("up", "--build", "--detach", "--wait", "--wait-timeout", "180")
        if result == 0:
            print("Open http://localhost:3000")
        return result
    if args.action == "down":
        return compose("down")
    if args.action == "config":
        return compose("config", "--quiet")
    return compose("logs", "--tail", "80", "backend", "frontend", "migrate", "seed")


if __name__ == "__main__":
    raise SystemExit(main())
