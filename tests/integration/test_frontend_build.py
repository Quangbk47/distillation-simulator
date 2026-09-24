"""Guard the public artifact boundary and reproducibility of the demo."""

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("frontend_build", ROOT / "scripts/build_frontend.py")
assert SPEC is not None and SPEC.loader is not None
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)


def test_build_is_reproducible_and_excludes_private_files(tmp_path: Path) -> None:
    (tmp_path / "web").mkdir()
    for name in BUILDER.ASSETS:
        (tmp_path / "web" / name).write_text("demo", encoding="utf-8")
    (tmp_path / "web/.env").write_text("private fixture", encoding="utf-8")
    (tmp_path / ".firebaserc").write_text('{"projects":{"default":"test-project"}}')
    first = BUILDER.build(tmp_path)
    assert BUILDER.build(tmp_path) == first
    output = tmp_path / "build/frontend"
    assert {p.name for p in output.iterdir()} == {*BUILDER.ASSETS, "build-info.json"}
    assert json.loads((output / "build-info.json").read_text())["build_id"] == first
    (tmp_path / "web/app.js").write_text("changed", encoding="utf-8")
    assert BUILDER.build(tmp_path) != first
    (output / "unexpected.txt").write_text("must not deploy")
    with pytest.raises(ValueError, match="Unexpected frontend output"):
        BUILDER.build(tmp_path)


def test_hosting_is_static_only() -> None:
    hosting = json.loads((ROOT / "firebase.json").read_text())["hosting"]
    assert hosting["public"] == "build/frontend"
    assert hosting["site"] == "distillation-simulator"
    assert "rewrites" not in hosting
    assert "functions" not in hosting
