"""Pure Raoult–Antoine helpers.

The coefficients are supplied by reviewed data records; this module deliberately
contains no component constants and no alternate VLE model.
"""

from dataclasses import dataclass
from math import pow


@dataclass(frozen=True)
class AntoineRecord:
    component: str
    A: float
    B: float
    C: float
    temperature_min: float
    temperature_max: float
    temperature_unit: str
    pressure_unit: str
    citation: str
    publication_version: str
    reviewer: str
    review_date: str | None


@dataclass(frozen=True)
class SaturationPressure:
    component: str
    temperature: float
    pressure: float
    pressure_unit: str
    is_extrapolated: bool
    warnings: tuple[str, ...]
    source_range: tuple[float, float]


def evaluate_antoine(record: AntoineRecord, temperature: float) -> SaturationPressure:
    """Evaluate one reviewed Antoine record and expose extrapolation explicitly."""

    if record.temperature_unit != "C":
        raise ValueError("V1 Antoine evaluation currently requires temperature_unit='C'")
    if temperature + record.C == 0:
        raise ValueError("Antoine denominator cannot be zero")

    pressure = pow(10.0, record.A - record.B / (temperature + record.C))
    if pressure <= 0:
        raise ValueError("Antoine evaluation produced a non-positive saturation pressure")

    extrapolated = not record.temperature_min <= temperature <= record.temperature_max
    warnings = ("THERMO_EXTRAPOLATION",) if extrapolated else ()
    return SaturationPressure(
        component=record.component,
        temperature=temperature,
        pressure=pressure,
        pressure_unit=record.pressure_unit,
        is_extrapolated=extrapolated,
        warnings=warnings,
        source_range=(record.temperature_min, record.temperature_max),
    )


def raoult_vapor_fraction(
    liquid_fraction: float,
    light_component_psat: float,
    heavy_component_psat: float,
    total_pressure: float,
) -> float:
    """Return the light-component vapor fraction from Raoult's law."""

    if not 0 <= liquid_fraction <= 1:
        raise ValueError("liquid_fraction must be between 0 and 1")
    if min(light_component_psat, heavy_component_psat, total_pressure) <= 0:
        raise ValueError("pressures must be positive")
    y = liquid_fraction * light_component_psat / total_pressure
    heavy_vapor_partial = (1 - liquid_fraction) * heavy_component_psat / total_pressure
    total_vapor_fraction = y + heavy_vapor_partial
    if total_vapor_fraction <= 0:
        raise ValueError("Raoult calculation produced a non-physical vapor fraction")
    return y / total_vapor_fraction
