from fastapi.testclient import TestClient

from api.app import app

client = TestClient(app)

VALID_SIMULATION_INPUT = {
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


def test_health_and_data_version_endpoints() -> None:
    assert client.get("/health").json() == {"status": "ok"}
    assert client.get("/api/thermo-data/version").json() == {
        "model": "raoult-antoine",
        "version": "NIST-SRD69-2026-10-04",
    }


def test_frontend_is_served_by_local_api() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "Distillation Simulator" in response.text


def test_total_condenser_simulation_returns_results() -> None:
    response = client.post("/api/simulations", json=VALID_SIMULATION_INPUT)
    assert response.status_code == 200
    body = response.json()
    assert body["status"] in {"success", "warning"}
    assert body["xD"] > body["xB"]
    assert body["residuals"]["solver"] < 1e-4
    assert len(body["stages"]) == 5
    assert body["operatingLines"]["feedIntersection"]["x"] == 0.5
    assert body["QC_kW"] is None
    assert body["QR_kW"] is None
    assert body["energyBreakdown"] is None
    assert body["warnings"] == ["THERMO_EXTRAPOLATION"]
    assert body["warningDetails"][0]["code"] == "THERMO_EXTRAPOLATION"
    assert "actualTemperature" in body["warningDetails"][0]
    assert body["warningDetails"][0]["sourceRange"]["unit"] == "K"


def test_simulation_rejects_unknown_input_fields() -> None:
    payload = VALID_SIMULATION_INPUT | {"unapprovedField": 1.0}

    response = client.post("/api/simulations", json=payload)

    assert response.status_code == 422


def test_simulation_rejects_feed_stage_above_total_stages() -> None:
    payload = VALID_SIMULATION_INPUT | {"N": 5, "NF": 6}

    response = client.post("/api/simulations", json=payload)

    assert response.status_code == 422
    assert "NF must be between 1 and N" in response.text


def test_simulation_rejects_distillate_flow_not_below_feed_flow() -> None:
    payload = VALID_SIMULATION_INPUT | {"F_kmol_h": 100.0, "D_kmol_h": 100.0}

    response = client.post("/api/simulations", json=payload)

    assert response.status_code == 422
    assert "D_kmol_h must be less than F_kmol_h" in response.text


def test_partial_condenser_is_explicitly_not_implemented() -> None:
    response = client.post(
        "/api/simulations",
        json={
            "F_kmol_h": 100.0,
            "zF_ethanol": 0.5,
            "q": 1.0,
            "P_bar": 1.0,
            "N": 10,
            "NF": 5,
            "R": 2.0,
            "D_kmol_h": 20.0,
            "heatLoss_kW": 0.0,
            "condenser": "partial",
        },
    )
    assert response.status_code == 501
    assert response.json()["detail"]["errorCode"] == "NOT_IMPLEMENTED"


def test_non_converged_total_condenser_returns_failed_result() -> None:
    response = client.post(
        "/api/simulations",
        json={
            "F_kmol_h": 100.0,
            "zF_ethanol": 0.5,
            "q": 1.0,
            "P_bar": 1.0,
            "N": 20,
            "NF": 10,
            "R": 2.0,
            "D_kmol_h": 45.2,
            "heatLoss_kW": 0.0,
            "condenser": "total",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "failed"
    assert body["errorCode"] == "NON_CONVERGED"
    assert body["errorMessage"].startswith("Calculation did not converge")
    assert body["xD"] is None
    assert body["xB"] is None
    assert body["stages"] == []


def test_sensitivity_is_structured_not_implemented_until_validation() -> None:
    response = client.post(
        "/api/sensitivity",
        json={
            "base": {
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
            },
            "parameter": "R",
            "values": [2.0, 3.0, 4.0],
        },
    )

    assert response.status_code == 501
    body = response.json()["detail"]
    assert body["status"] == "not_implemented"
    assert body["errorCode"] == "NOT_IMPLEMENTED"
    assert "approved validation case" in body["message"]
