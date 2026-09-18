import json
from pathlib import Path


def test_validation_is_not_reported_as_pass_before_signoff() -> None:
    path = Path(__file__).resolve().parents[2] / "data/validation/cases/ethanol-water.pending.json"
    case = json.loads(path.read_text(encoding="utf-8"))
    assert case["validationAcceptance"]["status"] == "PENDING_THRESHOLD"
    assert case["validationAcceptance"]["metric"] == "PENDING_EXPERT_THRESHOLD"
