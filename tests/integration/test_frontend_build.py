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
    assert hosting["site"] == "delta-pagoda-509904-j8"
    assert "rewrites" not in hosting
    assert "functions" not in hosting


def test_hosting_status_reads_the_deployed_build_project() -> None:
    script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
    assert "const project = info.project;" in script
    assert "`${project}.web.app`" in script


def test_frontend_renders_structured_failed_state() -> None:
    script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
    html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "web" / "styles.css").read_text(encoding="utf-8")

    assert "setResultStatus(result.status.toUpperCase())" in script
    assert "Chưa có stage output hợp lệ" in script
    assert "FAILED · Không có dữ liệu đồ thị hợp lệ" in script
    assert "function escapeHtml" in script
    assert "Bảng kết quả theo mâm" in html
    assert '.pending-badge[data-status="failed"]' in css


def test_frontend_keeps_unapproved_features_disabled() -> None:
    html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")

    assert '<option value="partial" disabled>Partial — Chưa hỗ trợ</option>' in html
    assert '<button class="button primary" type="button" disabled>Chạy khảo sát</button>' in html
    assert "energy pending" in html
