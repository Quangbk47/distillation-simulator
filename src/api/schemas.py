"""Typed API contracts shared by the backend and future clients."""

from math import isfinite
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class SimulationInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    F_kmol_h: float = Field(gt=0)
    zF_ethanol: float = Field(gt=0, lt=1)
    q: float
    P_bar: float = Field(gt=0)
    N: int = Field(ge=1)
    NF: int = Field(ge=1)
    R: float = Field(ge=0)
    D_kmol_h: float = Field(gt=0)
    heatLoss_kW: float = Field(ge=0)
    condenser: Literal["total", "partial"]

    @field_validator(
        "F_kmol_h",
        "zF_ethanol",
        "q",
        "P_bar",
        "R",
        "D_kmol_h",
        "heatLoss_kW",
    )
    @classmethod
    def validate_finite_numbers(cls, value: float) -> float:
        if not isfinite(value):
            raise ValueError("numeric inputs must be finite")
        return value

    @model_validator(mode="after")
    def validate_cross_field_constraints(self) -> "SimulationInput":
        if self.NF > self.N:
            raise ValueError("NF must be between 1 and N")
        if self.D_kmol_h >= self.F_kmol_h:
            raise ValueError("D_kmol_h must be less than F_kmol_h")
        return self


class ResidualModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    totalMass: float | None = None
    ethanolBalance: float | None = None
    outer: float | None = None
    solver: float | None = None


class StageResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    stage: int
    T_C: float
    x_ethanol: float
    y_ethanol: float
    section: Literal["rectifying", "stripping"]


class SimulationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["success", "warning", "failed", "not_implemented"]
    errorCode: str | None = None
    D_kmol_h: float | None = None
    B_kmol_h: float | None = None
    xD: float | None = None
    xB: float | None = None
    recovery_ethanol_percent: float | None = None
    thermoModel: Literal["raoult-antoine"]
    thermoDataVersion: str
    isExtrapolated: bool
    warnings: list[str]
    residuals: ResidualModel
    QC_kW: float | None = None
    QR_kW: float | None = None
    heatLoss_kW: float | None = None
    energyBreakdown: dict[str, float] | None = None
    operatingLines: dict[str, object] | None = None
    stages: list[StageResult] = Field(default_factory=list)
    trace: list[str] = Field(default_factory=list)


class SensitivityRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    base: SimulationInput
    parameter: Literal["R", "N", "NF"]
    values: list[float | int] = Field(min_length=1)
