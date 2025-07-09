# tests/test_endpoints.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_us_search():
    response = client.post("/search", json={"country": "US", "query": "iPhone 16 Pro, 128GB"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
