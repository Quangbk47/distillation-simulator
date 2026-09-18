"""Condenser mode contract for the McCabe–Thiele engine."""

from typing import Literal

CondenserMode = Literal["total", "partial"]


def validate_condenser_mode(mode: str) -> CondenserMode:
    if mode not in {"total", "partial"}:
        raise ValueError("condenser must be 'total' or 'partial'")
    return mode  # type: ignore[return-value]
