"""A fresh temporary database for every automated test."""
import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    # No test may alter the user's real minidash.db file.
    monkeypatch.setenv("MINIDASH_DB_PATH", str(tmp_path / "test.db"))
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def created_order(client):
    # A reusable valid purchase for tracking tests.
    response = client.post("/orders",json={"restaurant_id":1,"address":"123 Example St",
                                          "items":[{"menu_item_id":1,"quantity":2}]})
    assert response.status_code == 201
    return response.json()
