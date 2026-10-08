"""Quick local API smoke check for demo/handover.

This script uses FastAPI's in-process TestClient, so it does not require a
running Uvicorn server. It is intended as a fast sanity check before a local
demo, not as scientific validation.
"""

# ruff: noqa: E402, I001

from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from api.app import app  # noqa: E402


BASE_CASE = {
    "F_kmol_h": 100.0,
    "zF_ethanol": 0.5,
    "q": 1.0,
    "P_bar": 1.0,
    "N": 5,
    "NF": 2,
    "R": 3.0,
    "D_kmol_h": 80.0,
    "heatLoss_kW": 0.0,
    "condenser": "total",
}


def check(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"SMOKE FAIL: {message}")
    print(f"PASS: {message}")


def main() -> None:
    client = TestClient(app)

    health = client.get("/health")
    check(health.status_code == 200 and health.json() == {"status": "ok"}, "health endpoint")

    version = client.get("/api/thermo-data/version")
    version_body = version.json()
    check(version.status_code == 200, "thermo version endpoint")
    check(version_body["model"] == "raoult-antoine", "thermo model is Raoult + Antoine")
    check(version_body["version"] == "NIST-SRD69-2026-10-04", "reviewed thermo data version")

    simulation = client.post("/api/simulations", json=BASE_CASE)
    sim_body = simulation.json()
    check(simulation.status_code == 200, "total-condenser simulation endpoint")
    check(sim_body["status"] in {"success", "warning"}, "simulation returns success/warning")
    check(sim_body["xD"] > sim_body["xB"], "xD greater than xB")
    check(len(sim_body["stages"]) == BASE_CASE["N"], "stage table length matches N")
    check(sim_body["QC_kW"] is None and sim_body["QR_kW"] is None, "energy remains pending")

    invalid_feed_stage = client.post("/api/simulations", json={**BASE_CASE, "NF": 6})
    check(invalid_feed_stage.status_code == 422, "invalid NF>N input is rejected")

    extra_field = client.post(
        "/api/simulations", json={**BASE_CASE, "unapprovedField": 1.0}
    )
    check(extra_field.status_code == 422, "unapproved simulation fields are rejected")

    partial_case = {**BASE_CASE, "condenser": "partial"}
    partial = client.post("/api/simulations", json=partial_case)
    check(partial.status_code == 501, "partial condenser remains not implemented")
    check(partial.json()["detail"]["errorCode"] == "NOT_IMPLEMENTED", "partial error code")

    sensitivity = client.post(
        "/api/sensitivity",
        json={"base": BASE_CASE, "parameter": "R", "values": [2.0, 3.0, 4.0]},
    )
    check(sensitivity.status_code == 501, "sensitivity remains gated")
    check(sensitivity.json()["detail"]["errorCode"] == "NOT_IMPLEMENTED", "sensitivity error code")

    print("SMOKE PASS: local API contract is ready for demo.")


if __name__ == "__main__":
    main()
