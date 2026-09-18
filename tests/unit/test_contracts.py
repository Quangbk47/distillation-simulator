from api.schemas import SimulationInput
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
        "D": 20.0,
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


def test_all_residuals_are_required_for_success() -> None:
    assert residuals_pass(Residuals(0.0, 0.0, 0.0))
    assert not residuals_pass(Residuals(0.0, 0.0, 1e-4))


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
    assert result.source_range == (20.0, 80.0)
