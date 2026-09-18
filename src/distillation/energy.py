"""Pure energy-calculation boundary.

The actual enthalpy implementation must be added with cited Cp/latent-heat data.
It must treat heat loss as an absolute kW load and return an auditable breakdown.
"""

from collections.abc import Mapping


class EnergyCalculationNotReady(NotImplementedError):
    """Raised until reviewed enthalpy data and the calculation contract are wired."""


def calcEnergy(
    input: Mapping[str, object],
    solution: Mapping[str, object],
    enthalpyData: Mapping[str, object],
) -> dict[str, object]:
    """Reserved pure function required by ALGORITHM_SPEC."""

    del input, solution, enthalpyData
    raise EnergyCalculationNotReady(
        "Add reviewed Cp/latent-heat data before implementing QC/QR calculation"
    )


calc_energy = calcEnergy
