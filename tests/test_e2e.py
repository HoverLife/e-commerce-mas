from fastapi.testclient import TestClient
from main import app

def test_simulate():
    client = TestClient(app)
    res = client.post("/simulate", json=["electronics"])
    assert res.status_code == 200
    data = res.json()
    assert "state" in data
    assert isinstance(data["state"], dict)