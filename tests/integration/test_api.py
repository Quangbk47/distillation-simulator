from fastapi.testclient import TestClient

from api.app import app

client = TestClient(app)


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
    response = client.post(
        "/api/simulations",
        json={
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
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] in {"success", "warning"}
    assert body["xD"] > body["xB"]
    assert body["residuals"]["solver"] < 1e-4
    assert len(body["stages"]) == 5
    assert body["operatingLines"]["feedIntersection"]["x"] == 0.5
    assert body["warnings"] == ["THERMO_EXTRAPOLATION"]
    assert body["warningDetails"][0]["code"] == "THERMO_EXTRAPOLATION"
    assert "actualTemperature" in body["warningDetails"][0]
    assert body["warningDetails"][0]["sourceRange"]["unit"] == "K"


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
