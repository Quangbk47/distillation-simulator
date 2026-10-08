import json
from pathlib import Path

from scripts.check_validation_balance import check_case


def test_validation_is_not_reported_as_pass_before_case_evaluation() -> None:
    path = Path(__file__).resolve().parents[2] / "data/validation/cases/ethanol-water.pending.json"
    case = json.loads(path.read_text(encoding="utf-8"))
    assert case["validationAcceptance"]["status"] == "READY_FOR_EVALUATION"
    assert case["validationAcceptance"]["metric"] == "MAE_xD_xB_percentage_points"
    assert case["validationAcceptance"]["threshold"] == 5
    assert case["validationAcceptance"]["pass"] is None
    assert case["sourceConditions"]["massBalanceReview"]["status"] == "NEEDS_GVHD_CONFIRMATION"


def test_supervisor_candidate_balance_conflict_is_reproducible() -> None:
    path = Path(__file__).resolve().parents[2] / "data/validation/cases/ethanol-water.pending.json"
    case = json.loads(path.read_text(encoding="utf-8"))

    result = check_case(case)

    assert round(result.required_d_from_xd_xb, 2) == 49.89
    assert round(result.recovery_from_required_d, 2) == 94.79
    assert round(result.xb_from_input_d, 4) == 0.1288
    assert result.residual_abs > 1.0
