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
THERMO_MODEL = "raoult-antoine"
THERMO_VERSION = "NIST-SRD69-2026-10-04"


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/thermo-data/version")
def thermo_data_version() -> dict[str, str]:
    return {"model": THERMO_MODEL, "version": THERMO_VERSION}


def failed_simulation(error_code: str, message: str, simulation_input: SimulationInput) -> SimulationResult:
    return SimulationResult.model_validate(
        {
            "status": "failed",
            "errorCode": error_code,
            "errorMessage": message,
            "D_kmol_h": simulation_input.D_kmol_h,
            "B_kmol_h": simulation_input.F_kmol_h - simulation_input.D_kmol_h,
            "xD": None,
            "xB": None,
            "recovery_ethanol_percent": None,
            "thermoModel": THERMO_MODEL,
            "thermoDataVersion": THERMO_VERSION,
            "isExtrapolated": False,
            "warnings": [error_code],
            "warningDetails": [],
            "residuals": {
                "totalMass": None,
                "ethanolBalance": None,
                "outer": None,
                "solver": None,
            },
            "QC_kW": None,
            "QR_kW": None,
            "heatLoss_kW": simulation_input.heatLoss_kW,
            "energyBreakdown": None,
            "operatingLines": None,
            "stages": [],
            "trace": ["total condenser", "calculation failed before validated result"],
        }
    )


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
    except SimulationEngineNotReady as error:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail={
                "status": "not_implemented",
                "errorCode": "NOT_IMPLEMENTED",
                "message": str(error),
            },
        ) from error
    except ValueError as error:
        error_code = str(error) or "CALCULATION_FAILED"
        return failed_simulation(
            error_code=error_code,
            message=(
                "Calculation did not converge for this total-condenser input. "
                "Check mass balance, D, N/NF, reflux ratio and validation-case conventions."
            ),
            simulation_input=simulation_input,
        )
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
