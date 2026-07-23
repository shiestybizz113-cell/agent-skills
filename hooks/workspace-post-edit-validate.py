#!/usr/bin/env python3
import json
import os
import subprocess
import sys
from pathlib import Path


SKIP_DIRS = {
    ".claude",
    "node_modules",
    ".venv",
    ".next",
    "coverage",
    "dist",
    "build",
    "__pycache__",
}


def read_payload() -> dict:
    if sys.stdin.isatty():
        return {}
    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


def find_repo_root(file_path: Path, project_dir: Path) -> Path | None:
    current = file_path.parent
    while True:
        if any(
            (current / marker).exists()
            for marker in ("package.json", "pyproject.toml", "Cargo.toml", "go.mod", "pom.xml", ".git")
        ):
            return current
        if current == project_dir or current.parent == current:
            return None
        current = current.parent


def should_skip(file_path: Path) -> bool:
    return any(part in SKIP_DIRS for part in file_path.parts)


def shutil_which(binary: str) -> str | None:
    for directory in os.environ.get("PATH", "").split(os.pathsep):
        candidate = Path(directory) / binary
        if candidate.exists() and os.access(candidate, os.X_OK):
            return str(candidate)
    return None


def choose_command(repo_root: Path) -> list[str] | None:
    package_json = repo_root / "package.json"
    pyproject = repo_root / "pyproject.toml"

    if package_json.exists():
        try:
            data = json.loads(package_json.read_text(encoding="utf-8"))
        except Exception:
            return None
        scripts = data.get("scripts", {})
        if "typecheck" in scripts:
            return ["npm", "run", "typecheck"]
        if "lint" in scripts:
            return ["npm", "run", "lint"]
        if "build" in scripts:
            return ["npm", "run", "build"]
        if "test" in scripts:
            return ["npm", "run", "test"]

    if pyproject.exists() or (repo_root / "pytest.ini").exists():
        if (repo_root / "tests").exists():
            if shutil_which("pytest"):
                return ["pytest", "-q"]
            return ["python3", "-m", "pytest", "-q"]
        return ["python3", "-m", "compileall", str(repo_root)]

    return None


def main() -> int:
    payload = read_payload()
    file_path_raw = payload.get("tool_input", {}).get("file_path")
    project_dir_raw = os.environ.get("CLAUDE_PROJECT_DIR")

    if not file_path_raw or not project_dir_raw:
        return 0

    file_path = Path(file_path_raw)
    project_dir = Path(project_dir_raw)

    if should_skip(file_path):
        return 0

    repo_root = find_repo_root(file_path, project_dir)
    if not repo_root:
        return 0

    command = choose_command(repo_root)
    if not command:
        return 0

    try:
        result = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
    except Exception as exc:
        print(f"[workspace-validate] skipped for {repo_root}: {exc}", file=sys.stderr)
        return 0

    print(
        f"[workspace-validate] {repo_root}: {' '.join(command)} -> {result.returncode}",
        file=sys.stderr,
    )

    if result.returncode != 0:
        stderr = (result.stderr or "").strip()
        stdout = (result.stdout or "").strip()
        detail = stderr or stdout
        if detail:
            print(detail[:2000], file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
