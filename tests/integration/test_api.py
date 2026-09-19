from fastapi.testclient import TestClient

from api.app import app

client = TestClient(app)


def test_health_and_data_version_endpoints() -> None:
    assert client.get("/health").json() == {"status": "ok"}
    assert client.get("/api/thermo-data/version").json() == {
        "model": "raoult-antoine",
        "version": "PENDING_REVIEW",
    }


def test_simulation_endpoint_is_not_claimed_ready() -> None:
    response = client.post("/api/simulations", json={})
    assert response.status_code == 422


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
