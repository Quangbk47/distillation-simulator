"""McCabe–Thiele engine boundary; no simulation values are hard-coded here."""

from typing import NoReturn

from .contracts import SimulationCase


class SimulationEngineNotReady(NotImplementedError):
    """Raised while the reviewed thermo data and closed stage solver are pending."""


def solve_mccabe_thiele(simulation_input: SimulationCase) -> NoReturn:
    """Reserve the deterministic V1 engine entry point.

    The implementation must solve the scalar xD outer residual and enforce
    NF consistency as documented in ``docs/PROCESS_MODEL.md``. Energy data is
    not a prerequisite for this VLE/stage boundary.
    """

    del simulation_input
    raise SimulationEngineNotReady(
        "Implement Raoult–Antoine, McCabe–Thiele, condenser branches and energy gates"
    )
