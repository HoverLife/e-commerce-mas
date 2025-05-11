from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_simulate_endpoint():
    response = client.get("/simulate?count=3")
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert "ctr" in data
    assert isinstance(data["recommendations"], list)
    assert 0.0 <= data["ctr"] <= 1.0
