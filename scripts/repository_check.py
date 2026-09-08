"""Check handoff completeness, exact trace IDs and task DAG; hash/package clean sources."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TEXT_ENCODING = "utf-8"
CSV_ENCODING = "utf-8-sig"

EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "node_modules",
    ".next",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "test-results",
    "playwright-report",
    "local-checks",
    "dist",
    "build",
}

REQUIRED = [
    "README.md",
    "AGENTS.md",
    "HANDOFF_TO_CODEX.md",
    "LICENSE_NOTE.md",
    ".env.example",
    "docker-compose.yml",
    "Makefile",
    "pyproject.toml",
    "uv.lock",
    "frontend/package-lock.json",
    "backend/Dockerfile",
    "frontend/Dockerfile",
    "DEMO_DEPLOYMENT.md",
    ".railway/railway.ts",
    ".railway/package-lock.json",
    ".github/workflows/ci.yml",
    "docs/tasks/M1-01.md",
    "validation/STARTER_AUDIT.md",
    "validation/REQUIREMENT_COVERAGE.md",
    "validation/FINAL_DELIVERY_REPORT.md",
]

REQUIRED += [
    f"docs/{name}.md"
    for name in [
        "POC_CONTRACT",
        "REQUIREMENT_TRACE",
        "ARCHITECTURE",
        "DOMAIN_MODEL",
        "OPD_WORKFLOW",
        "ACCEPTANCE_TESTS",
        "SECURITY_BOUNDARY",
        "FHIR_MAPPING",
        "EVENT_MODEL",
        "OPEN_QUESTIONS",
        "LEARNING_GUIDE",
        "MILESTONES",
        "LOCAL_VALIDATION",
        "DEPENDENCIES",
    ]
]

REQUIRED += [
    f".ai/{name}.md"
    for name in [
        "ORCHESTRATOR",
        "BUILDER",
        "SRS_GUARDIAN",
        "REVIEWER",
        "ROUTING_POLICY",
        "TASK_TEMPLATE",
        "FINDING_TEMPLATE",
        "RUN_RECORD_TEMPLATE",
    ]
]


def read_text(path: Path) -> str:
    """Read repository text deterministically as UTF-8."""
    return path.read_text(encoding=TEXT_ENCODING)


def read_json(path: Path) -> dict | list:
    """Read UTF-8 JSON without depending on the host OS locale."""
    return json.loads(read_text(path))


def clean_files(*, include_evidence: bool = False) -> list[Path]:
    result: list[Path] = []

    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)

        if not path.is_file() or path.is_symlink():
            continue

        if any(part in EXCLUDED_DIRS for part in relative.parts):
            # Retained check transcripts are small and intentionally
            # included in delivery when evidence packaging is requested.
            if not (include_evidence and relative.parts[:2] == ("validation", "local-checks")):
                continue

        if relative.parts[:2] == (".ai", "runs") and path.name != ".gitkeep":
            continue

        if not include_evidence and relative.parts[0] == "validation":
            continue

        if path.name.startswith(".env") and path.name != ".env.example":
            continue

        if path.suffix.lower() in {
            ".pyc",
            ".pyo",
            ".zip",
            ".tsbuildinfo",
            ".log",
        }:
            continue

        result.append(path)

    return sorted(result)


def candidate_digest() -> str:
    digest = hashlib.sha256()

    for path in clean_files():
        relative = path.relative_to(ROOT).as_posix()

        digest.update(relative.encode("utf-8") + b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())

    return digest.hexdigest()


def verify() -> list[str]:
    errors: list[str] = []

    # Required repository files.
    for required in REQUIRED:
        if not (ROOT / required).is_file():
            errors.append(f"Missing required file: {required}")

    # Avoid secondary traceback noise if required source files are missing.
    trace_path = ROOT / "docs/REQUIREMENT_TRACE.md"
    selected_requirements_path = ROOT / "docs/source/selected_requirements.json"
    module_inventory_path = ROOT / "docs/source/module_inventory_53.csv"
    tasks_path = ROOT / "docs/tasks/tasks.json"

    if not trace_path.is_file():
        return errors

    if not selected_requirements_path.is_file():
        errors.append("Missing required source file: docs/source/selected_requirements.json")
        return errors

    if not module_inventory_path.is_file():
        errors.append("Missing required source file: docs/source/module_inventory_53.csv")
        return errors

    if not tasks_path.is_file():
        errors.append("Missing required task index: docs/tasks/tasks.json")
        return errors

    # Exact requirement trace validation.
    trace = read_text(trace_path)
    data = read_json(selected_requirements_path)

    if not isinstance(data, dict):
        errors.append("selected_requirements.json must contain a JSON object")
        return errors

    requirements = data.get("requirements")
    expected_count = data.get("requirement_count")

    if not isinstance(requirements, list):
        errors.append("selected_requirements.json: 'requirements' must be a list")
        requirements = []

    identifiers = {
        row["srs_id"]
        for row in requirements
        if isinstance(row, dict) and isinstance(row.get("srs_id"), str) and row["srs_id"].strip()
    }

    if len(identifiers) != expected_count or len(identifiers) != 153:
        errors.append("Exact selected-source requirement count changed without reconciliation")

    for identifier in sorted(identifiers):
        pattern = r"(?<![A-Z0-9-])" + re.escape(identifier) + r"(?![A-Z0-9-])"

        if not re.search(pattern, trace):
            errors.append(f"Missing exact trace identifier: {identifier}")

    # 53-module inventory.
    #
    # utf-8-sig accepts normal UTF-8 as well as UTF-8 files containing a BOM.
    with module_inventory_path.open(
        mode="r",
        encoding=CSV_ENCODING,
        newline="",
    ) as source:
        module_rows = list(csv.DictReader(source))

    if len(module_rows) != 53:
        errors.append(f"Module inventory must account for 53 modules (found {len(module_rows)})")

    # Task DAG.
    tasks = read_json(tasks_path)

    if not isinstance(tasks, list):
        errors.append("docs/tasks/tasks.json must contain a JSON array")
        tasks = []

    task_ids = [task.get("id") for task in tasks if isinstance(task, dict)]

    if len(task_ids) != len(set(task_ids)):
        errors.append("Duplicate task IDs")

    graph: dict[str, list[str]] = {}

    for task in tasks:
        if not isinstance(task, dict):
            errors.append("Invalid task entry: expected JSON object")
            continue

        task_id = task.get("id")
        depends_on = task.get("depends_on", [])

        if not isinstance(task_id, str) or not task_id:
            errors.append("Task entry missing valid id")
            continue

        if not isinstance(depends_on, list):
            errors.append(f"Task {task_id}: depends_on must be a list")
            continue

        graph[task_id] = depends_on

    visited: set[str] = set()
    visiting: set[str] = set()

    def visit(task_id: str) -> None:
        if task_id not in graph:
            errors.append(f"Unknown task dependency: {task_id}")
            return

        if task_id in visiting:
            errors.append(f"Task cycle: {task_id}")
            return

        if task_id in visited:
            return

        visiting.add(task_id)

        for parent in graph[task_id]:
            if not isinstance(parent, str):
                errors.append(f"Task {task_id}: dependency must be a string")
                continue

            visit(parent)

        visiting.remove(task_id)
        visited.add(task_id)

    for task_id in graph:
        visit(task_id)

    for task in tasks:
        if not isinstance(task, dict):
            continue

        task_id = task.get("id")
        task_path = task.get("path")

        if not isinstance(task_id, str):
            continue

        if not isinstance(task_path, str) or not task_path:
            errors.append(f"Task {task_id}: missing task contract path")
            continue

        if not (ROOT / task_path).is_file():
            errors.append(f"Missing task contract: {task_id}")

    # Secret scanning.
    #
    # Files in clean_files may include binary assets. Decode strictly when
    # possible, and skip undecodable binary files rather than depending on
    # the Windows locale.
    secret_pattern = re.compile(
        r"sk-(?:or-v1-)?[A-Za-z0-9]{30,}|"
        r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----"
    )

    for path in clean_files(include_evidence=True):
        try:
            text = path.read_text(encoding=TEXT_ENCODING)
        except UnicodeDecodeError:
            # Binary/non-UTF-8 file; it is already handled byte-for-byte
            # by packaging/digest logic.
            continue

        if secret_pattern.search(text):
            errors.append(f"Potential secret signature in {path.relative_to(ROOT).as_posix()}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "--digest",
        action="store_true",
        help="Print deterministic candidate SHA-256 after verification",
    )

    parser.add_argument(
        "--package",
        type=Path,
        help="Write clean review candidate ZIP after checks",
    )

    args = parser.parse_args()

    errors = verify()

    if errors:
        print("\n".join(errors))
        return 1

    print(
        "PASS: required files, 53 modules, 153 exact IDs, "
        "task DAG and secret signatures "
        f"({len(clean_files())} source files)"
    )

    if args.digest:
        print("candidate_sha256=" + candidate_digest())

    if args.package:
        args.package.parent.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(
            args.package,
            "w",
            zipfile.ZIP_DEFLATED,
        ) as archive:
            for path in clean_files(include_evidence=True):
                archive_path = "omnimed-poc/" + path.relative_to(ROOT).as_posix()

                info = zipfile.ZipInfo(
                    archive_path,
                    (2026, 9, 8, 0, 0, 0),
                )
                info.external_attr = 0o100644 << 16

                archive.writestr(
                    info,
                    path.read_bytes(),
                    compress_type=zipfile.ZIP_DEFLATED,
                )

        print("Wrote clean review candidate:", args.package.name)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
