"""Sensitivity contract preserving V1 invariants."""

from typing import Literal

from distillation.contracts import SimulationCase

SensitivityParameter = Literal["R", "N", "NF"]


def validate_parameter(parameter: str) -> SensitivityParameter:
    if parameter not in {"R", "N", "NF"}:
        raise ValueError("Sensitivity may vary exactly one of R, N or NF")
    return parameter  # type: ignore[return-value]


def preserve_fixed_inputs(simulation_input: SimulationCase) -> tuple[float, str, float]:
    """Return q, condenser and absolute heat loss that a sweep must preserve."""

    return simulation_input.q, simulation_input.condenser, simulation_input.heatLoss_kW
