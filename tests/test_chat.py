import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_invalid_command():
    r = client.post("/chat", json={"message": "Привет!"})
    assert r.status_code == 400

def test_unknown_category():
    r = client.post("/chat", json={"message": "Покажи товары категории no_such"})
    assert r.status_code == 200
    data = r.json()
    assert "response" in data and "не найдена" in data["response"].lower()

def test_known_category():
    # Предполагаем, что в БД есть agro_industry_and_commerce
    r = client.post("/chat", json={"message": "Покажи товары категории agro_industry_and_commerce"})
    assert r.status_code == 200
    data = r.json()
    assert "items" in data and isinstance(data["items"], list)
