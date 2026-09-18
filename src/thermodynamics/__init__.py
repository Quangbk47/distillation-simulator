"""Thermodynamic data contracts and the V1 Raoult–Antoine model."""

from .antoine_raoult import (
    AntoineRecord,
    SaturationPressure,
    evaluate_antoine,
    raoult_vapor_fraction,
)

__all__ = ["AntoineRecord", "SaturationPressure", "evaluate_antoine", "raoult_vapor_fraction"]
