from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/teams")
    assert response.status_code == 200
    print(response.json())