"""FastAPI boundary; calculation authority stays in the backend engine."""

from fastapi import FastAPI, HTTPException, status

from .schemas import SensitivityRequest, SimulationInput, SimulationResult

app = FastAPI(title="Distillation Simulator API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/thermo-data/version")
def thermo_data_version() -> dict[str, str]:
    return {"model": "raoult-antoine", "version": "PENDING_REVIEW"}


@app.post("/api/simulations", response_model=SimulationResult)
def create_simulation(simulation_input: SimulationInput) -> SimulationResult:
    if simulation_input.condenser == "partial":
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail={
                "status": "not_implemented",
                "errorCode": "NOT_IMPLEMENTED",
                "message": "Partial-condenser calculation contract is open and blocked",
            },
        )
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="V1 calculation engine is not implemented in the repository skeleton",
    )


@app.post("/api/sensitivity")
def create_sensitivity(request: SensitivityRequest) -> dict[str, str]:
    del request
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Sensitivity runner is reserved for the V1 engine implementation",
    )
