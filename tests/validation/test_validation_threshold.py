import json
from pathlib import Path


def test_validation_is_not_reported_as_pass_before_case_evaluation() -> None:
    path = Path(__file__).resolve().parents[2] / "data/validation/cases/ethanol-water.pending.json"
    case = json.loads(path.read_text(encoding="utf-8"))
    assert case["validationAcceptance"]["status"] == "READY_FOR_EVALUATION"
    assert case["validationAcceptance"]["metric"] == "MAE_xD_xB_percentage_points"
    assert case["validationAcceptance"]["threshold"] == 5
    assert case["validationAcceptance"]["pass"] is None
