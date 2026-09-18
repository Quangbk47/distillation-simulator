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
