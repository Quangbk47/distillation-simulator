from api.schemas import SimulationInput
from distillation.mccabe_thiele import q_line_intersection, select_ethanol_record
from solver.convergence import Residuals, residuals_pass
from thermodynamics.antoine_raoult import AntoineRecord, evaluate_antoine


def valid_input(**overrides: object) -> SimulationInput:
    values: dict[str, object] = {
        "F_kmol_h": 100.0,
        "zF_ethanol": 0.5,
        "q": 1.0,
        "P_bar": 1.0,
        "N": 10,
        "NF": 5,
        "R": 2.0,
        "D_kmol_h": 20.0,
        "heatLoss_kW": 0.0,
        "condenser": "total",
    }
    values.update(overrides)
    return SimulationInput.model_validate(values)


def test_q_is_direct_and_heat_loss_is_absolute() -> None:
    item = valid_input(q=0.35, heatLoss_kW=12.5)
    assert item.q == 0.35
    assert item.heatLoss_kW == 12.5


def test_feed_stage_and_condenser_contract() -> None:
    assert valid_input(condenser="partial").condenser == "partial"
    try:
        valid_input(N=3, NF=4)
    except ValueError as error:
        assert "NF" in str(error)
    else:
        raise AssertionError("NF > N must be rejected")


def test_simulation_flow_constraints_are_not_degenerate() -> None:
    for overrides in ({"D_kmol_h": 0.0}, {"D_kmol_h": 100.0}, {"zF_ethanol": 0.0}):
        try:
            valid_input(**overrides)
        except ValueError:
            pass
        else:
            raise AssertionError("degenerate simulation flow/composition must be rejected")


def test_all_residuals_are_required_for_success() -> None:
    assert residuals_pass(Residuals(0.0, 0.0, 0.0, 0.0))
    assert not residuals_pass(Residuals(0.0, 0.0, 1e-4, 0.0))


def test_antoine_extrapolation_is_structured_warning() -> None:
    record = AntoineRecord(
        component="fixture-component",
        A=1.0,
        B=10.0,
        C=1.0,
        temperature_min=20.0,
        temperature_max=80.0,
        temperature_unit="C",
        pressure_unit="bar",
        citation="fixture citation",
        publication_version="fixture",
        reviewer="fixture reviewer",
        review_date="2026-09-18",
    )
    result = evaluate_antoine(record, 100.0)
    assert result.is_extrapolated
    assert result.warnings == ("THERMO_EXTRAPOLATION",)
    assert result.warning_details[0].component == "fixture-component"
    assert result.warning_details[0].actual_temperature == 100.0
    assert result.source_range == (20.0, 80.0)


def test_q_line_intersection_uses_approved_formula() -> None:
    xq, yq = q_line_intersection(z_feed=0.5, q=0.8, rect_slope=2 / 3, rect_intercept=0.3)

    assert round(xq, 12) == round((0.5 + (0.8 - 1.0) * 0.3) / (0.8 - (0.8 - 1.0) * 2 / 3), 12)
    assert round(yq, 12) == round((2 / 3) * xq + 0.3, 12)


def test_q_line_intersection_handles_saturated_liquid_without_division() -> None:
    xq, yq = q_line_intersection(z_feed=0.5, q=1.0, rect_slope=2 / 3, rect_intercept=0.3)

    assert xq == 0.5
    assert round(yq, 12) == round((2 / 3) * 0.5 + 0.3, 12)


def test_ethanol_record_selection_prefers_record_one_in_overlap() -> None:
    record_one = AntoineRecord(
        component="ethanol",
        A=5.24677,
        B=1598.673,
        C=-46.424,
        temperature_min=292.77,
        temperature_max=366.63,
        temperature_unit="K",
        pressure_unit="bar",
        citation="record one",
        publication_version="fixture",
        reviewer="fixture reviewer",
        review_date="2026-10-04",
    )
    record_two = AntoineRecord(
        component="ethanol",
        A=4.92531,
        B=1432.526,
        C=-61.819,
        temperature_min=364.80,
        temperature_max=513.91,
        temperature_unit="K",
        pressure_unit="bar",
        citation="record two",
        publication_version="fixture",
        reviewer="fixture reviewer",
        review_date="2026-10-04",
    )

    assert select_ethanol_record([record_one, record_two], 365.0) is record_one
    assert select_ethanol_record([record_one, record_two], 370.0) is record_two
