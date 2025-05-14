import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_chat_endpoint():
    payload = {"message": "Покажи товары категории agro_industry_and_commerce"}
    res = client.post("/chat", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "session_id" in data
    assert "response" in data
    assert isinstance(data["response"], str) 