"""Typed API contracts shared by the backend and future clients."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SimulationInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    F_kmol_h: float = Field(gt=0)
    zF_ethanol: float = Field(ge=0, le=1)
    q: float
    P_bar: float = Field(gt=0)
    N: int = Field(ge=1)
    NF: int = Field(ge=1)
    R: float = Field(ge=0)
    D: float = Field(ge=0)
    heatLoss_kW: float = Field(ge=0)
    condenser: Literal["total", "partial"]

    @model_validator(mode="after")
    def validate_feed_stage(self) -> "SimulationInput":
        if self.NF > self.N:
            raise ValueError("NF must be between 1 and N")
        return self


class ResidualModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    totalMass: float
    ethanolBalance: float
    solver: float


class SimulationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["success", "warning", "failed", "not_implemented"]
    thermoModel: Literal["raoult-antoine"]
    thermoDataVersion: str
    isExtrapolated: bool
    warnings: list[str]
    residuals: ResidualModel
    QC_kW: float | None = None
    QR_kW: float | None = None
    heatLoss_kW: float | None = None
    energyBreakdown: dict[str, float] | None = None
    trace: list[str] = Field(default_factory=list)


class SensitivityRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    base: SimulationInput
    parameter: Literal["R", "N", "NF"]
    values: list[float | int] = Field(min_length=1)
