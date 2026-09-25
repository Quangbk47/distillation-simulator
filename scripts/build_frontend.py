"""Build the static demo with reproducible public asset metadata."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ("index.html", "styles.css", "app.js")


def build(root: Path = ROOT) -> str:
    source = root / "web"
    target = root / "build" / "frontend"
    # Reject stale/unexpected output rather than silently publishing extra files.
    allowed = {*ASSETS, "build-info.json"}
    if target.exists() and any(p.name not in allowed or p.is_dir() for p in target.iterdir()):
        raise ValueError("Unexpected frontend output; inspect build/frontend before rebuilding")
    content = {name: (source / name).read_text(encoding="utf-8") for name in ASSETS}
    digest = hashlib.sha256()
    target.mkdir(parents=True, exist_ok=True)
    for name, value in content.items():
        data = value.encode("utf-8")
        digest.update(name.encode() + b"\0" + data + b"\0")
        (target / name).write_bytes(data)
    build_id = digest.hexdigest()
    project = json.loads((root / ".firebaserc").read_text())["projects"]["default"]
    (target / "build-info.json").write_text(
        json.dumps({"project": project, "build_id": build_id, "mode": "DEMO"}, indent=2) + "\n",
        encoding="utf-8",
    )
    return build_id


if __name__ == "__main__":
    print(f"Frontend build: {build()}")
