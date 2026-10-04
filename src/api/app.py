"""FastAPI boundary; calculation authority stays in the backend engine."""

from pathlib import Path

from fastapi import FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles

from distillation.contracts import SimulationCase
from distillation.mccabe_thiele import SimulationEngineNotReady, solve_mccabe_thiele

from .schemas import SensitivityRequest, SimulationInput, SimulationResult

app = FastAPI(title="Distillation Simulator API", version="0.1.0")
ROOT = Path(__file__).resolve().parents[2]
FRONTEND_BUILD = ROOT / "build/frontend"


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/thermo-data/version")
def thermo_data_version() -> dict[str, str]:
    return {"model": "raoult-antoine", "version": "NIST-SRD69-2026-10-04"}


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
    try:
        data = solve_mccabe_thiele(SimulationCase(**simulation_input.model_dump()))
    except (ValueError, SimulationEngineNotReady) as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)
        ) from error
    return SimulationResult.model_validate(data)


@app.post("/api/sensitivity")
def create_sensitivity(request: SensitivityRequest) -> dict[str, str]:
    del request
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Sensitivity runner is reserved for the V1 engine implementation",
    )


if (FRONTEND_BUILD / "index.html").exists():
    app.mount("/", StaticFiles(directory=FRONTEND_BUILD, html=True), name="frontend")
