"""Domain-level contracts independent from the HTTP/API layer."""

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class SimulationCase:
    F_kmol_h: float
    zF_ethanol: float
    q: float
    P_bar: float
    N: int
    NF: int
    R: float
    D_kmol_h: float
    heatLoss_kW: float
    condenser: Literal["total", "partial"]
