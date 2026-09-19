"""Fail fast when the repository loses a required V1 boundary."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_DIRECTORIES = (
    "docs",
    "data/thermodynamics",
    "data/validation",
    "src/thermodynamics",
    "src/distillation",
    "src/solver",
    "src/sensitivity",
    "src/api",
    "src/ui",
    "web",
    "tests/unit",
    "tests/integration",
    "tests/reference",
    "tests/validation",
    ".github/workflows",
)


def main() -> None:
    missing = [path for path in REQUIRED_DIRECTORIES if not (ROOT / path).is_dir()]
    if missing:
        raise SystemExit(f"Missing required directories: {', '.join(missing)}")
    if not (ROOT / ".env.example").is_file():
        raise SystemExit("Missing .env.example")
    if not (ROOT / "scripts/build_frontend.py").is_file():
        raise SystemExit("Missing scripts/build_frontend.py")
    print("Repository structure is complete.")


if __name__ == "__main__":
    main()
