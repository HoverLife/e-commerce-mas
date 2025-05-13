from fastapi.testclient import TestClient
from main import app

def test_simulate_endpoint():
    client = TestClient(app)
    res = client.post("/simulate")
    assert res.status_code == 200
    data = res.json()
    # Проверяем структуру
    assert "messages" in data and "agreement" in data
    assert isinstance(data["messages"], list)
    for msg in data["messages"]:
        assert "sender" in msg and "text" in msg
    # Должны быть и Buyer, и Seller
    assert any(m["sender"] == "Buyer" for m in data["messages"])
    assert any(m["sender"] == "Seller" for m in data["messages"])
