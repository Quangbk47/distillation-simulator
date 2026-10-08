"""Run the local quality gate with the current Python interpreter."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable

COMMANDS = (
    ("repository structure", [PYTHON, "scripts/check_structure.py"]),
    ("frontend build", [PYTHON, "scripts/build_frontend.py"]),
    ("ruff lint", [PYTHON, "-m", "ruff", "check", "."]),
    ("mypy", [PYTHON, "-m", "mypy", "src"]),
    (
        "pytest",
        [
            PYTHON,
            "-m",
            "pytest",
            "--basetemp",
            str(ROOT / "work/pytest-tmp"),
            "-p",
            "no:cacheprovider",
        ],
    ),
    ("local API smoke", [PYTHON, "scripts/smoke_local_api.py"]),
)


def main() -> None:
    for label, command in COMMANDS:
        print(f"\n==> {label}", flush=True)
        subprocess.run(command, cwd=ROOT, check=True)
    print("\nQUALITY PASS: local gate completed successfully.", flush=True)


if __name__ == "__main__":
    main()
