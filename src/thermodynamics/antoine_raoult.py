"""Pure Raoult–Antoine helpers.

The coefficients are supplied by reviewed data records; this module deliberately
contains no component constants and no alternate VLE model.
"""

from dataclasses import dataclass
from math import isfinite, pow


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
    formula: str = "log10(P) = A - B/(T + C)"


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

    if record.temperature_unit not in {"C", "K"}:
        raise ValueError("Antoine evaluation requires temperature_unit='C' or 'K'")
    if temperature + record.C == 0:
        raise ValueError("Antoine denominator cannot be zero")

    pressure = pow(10.0, record.A - record.B / (temperature + record.C))
    if not isfinite(pressure) or pressure <= 0:
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


def bubble_temperature(
    liquid_fraction: float,
    pressure_bar: float,
    light: AntoineRecord,
    heavy: AntoineRecord,
) -> tuple[float, tuple[str, ...]]:
    """Solve the binary Raoult bubble point by bisection."""
    if not 0.0 <= liquid_fraction <= 1.0 or pressure_bar <= 0:
        raise ValueError("invalid VLE input")
    lo = max(light.temperature_min, heavy.temperature_min)
    hi = min(light.temperature_max, heavy.temperature_max)
    if hi <= lo:
        raise ValueError("Antoine temperature ranges do not overlap")

    def f(t: float) -> float:
        pl = evaluate_antoine(light, t).pressure
        ph = evaluate_antoine(heavy, t).pressure
        return liquid_fraction * pl + (1.0 - liquid_fraction) * ph - pressure_bar

    flo, fhi = f(lo), f(hi)
    if flo * fhi > 0:
        # NIST ranges are source ranges, not hard runtime bounds. Extend the
        # bracket only for the root search; evaluate_antoine records the warning.
        lo -= 50.0
        hi += 50.0
        flo, fhi = f(lo), f(hi)
    if flo * fhi > 0:
        raise ValueError("bubble point is outside the supported Antoine bracket")
    for _ in range(40):
        mid = (lo + hi) / 2.0
        if abs(f(mid)) < 1e-9:
            break
        if flo * f(mid) <= 0:
            hi = mid
        else:
            lo, flo = mid, f(mid)
    result = evaluate_antoine(light, mid)
    other = evaluate_antoine(heavy, mid)
    return mid, tuple(dict.fromkeys(result.warnings + other.warnings))


def equilibrium_y(
    liquid_fraction: float, pressure_bar: float, light: AntoineRecord, heavy: AntoineRecord
) -> tuple[float, float, tuple[str, ...]]:
    temperature, warnings = bubble_temperature(liquid_fraction, pressure_bar, light, heavy)
    pl = evaluate_antoine(light, temperature).pressure
    y = liquid_fraction * pl / pressure_bar
    return y, temperature, warnings
