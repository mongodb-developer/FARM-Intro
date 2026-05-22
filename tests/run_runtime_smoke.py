#!/usr/bin/env python3
"""Repository runtime smoke test.

This test intentionally avoids external services and validates:
1) repo has at least one runnable/build marker
2) Python source files in repo compile successfully
"""

from __future__ import annotations

from pathlib import Path
import py_compile
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]

SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
    "__pycache__",
}


def has_runnable_marker(root: Path) -> bool:
    markers = [
        "package.json",
        "pyproject.toml",
        "requirements.txt",
        "setup.py",
        "manage.py",
        "pom.xml",
        "build.gradle",
        "build.gradle.kts",
        "go.mod",
        "Cargo.toml",
        "Dockerfile",
        "docker-compose.yml",
        "docker-compose.yaml",
        "Makefile",
    ]
    for marker in markers:
        if list(root.rglob(marker)):
            return True

    if list(root.rglob("*.csproj")) or list(root.rglob("*.sln")):
        return True

    return False


def iter_python_files(root: Path):
    for py_file in root.rglob("*.py"):
        rel = py_file.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        yield py_file


def main() -> int:
    if not has_runnable_marker(REPO_ROOT):
        print("FAIL: no runnable/build marker found")
        return 1

    py_files = list(iter_python_files(REPO_ROOT))
    if not py_files:
        print("PASS: no python files to compile; marker checks passed")
        return 0

    failures = []
    for py_file in py_files:
        try:
            py_compile.compile(str(py_file), doraise=True)
        except py_compile.PyCompileError as exc:
            failures.append((py_file, exc.msg))

    if failures:
        print(f"FAIL: {len(failures)} python files failed to compile")
        for py_file, msg in failures[:20]:
            rel = py_file.relative_to(REPO_ROOT)
            print(f"  - {rel}: {msg}")
        return 1

    print(f"PASS: compiled {len(py_files)} python files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
