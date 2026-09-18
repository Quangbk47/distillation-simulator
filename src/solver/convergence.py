"""V1 success gate for balances and solver convergence."""

from dataclasses import dataclass

SOLVER_TOLERANCE = 1e-4


@dataclass(frozen=True)
class Residuals:
    total_mass: float
    ethanol_balance: float
    solver: float

    def below_tolerance(self, tolerance: float = SOLVER_TOLERANCE) -> bool:
        return max(self.total_mass, self.ethanol_balance, self.solver) < tolerance


def residuals_pass(residuals: Residuals, tolerance: float = SOLVER_TOLERANCE) -> bool:
    """Return true only when every required residual is strictly below the gate."""

    return residuals.below_tolerance(tolerance)
