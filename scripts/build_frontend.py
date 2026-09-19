"""Copy the dependency-free V1 frontend into the Firebase-ready build folder."""

from pathlib import Path
from shutil import copy2

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "web"
TARGET = ROOT / "build" / "frontend"


def main() -> None:
    if not SOURCE.is_dir():
        raise SystemExit(f"Missing frontend source directory: {SOURCE}")
    TARGET.mkdir(parents=True, exist_ok=True)
    for source_file in SOURCE.iterdir():
        if source_file.is_file():
            copy2(source_file, TARGET / source_file.name)
    print(f"Frontend built to {TARGET}")


if __name__ == "__main__":
    main()
