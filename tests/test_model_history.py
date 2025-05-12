import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.main import app

client = TestClient(app)

@pytest.fixture
def mock_db():
    with patch("src.database.InMemoryDatabase") as mock_db_class:
        mock_db_instance = MagicMock()
        mock_collection = MagicMock()
        mock_collection.find.return_value = [{"prediction": 42.0}]
        mock_db_instance.get_collection.return_value = mock_collection
        mock_db_class.return_value = mock_db_instance
        yield mock_db_instance

def test_history(mock_db):
    response = client.get("/model/history/")
    print(response)
    print(response.json())
    assert response.status_code == 200
    assert "history" in response.json()
    assert isinstance(response.json()["history"], list)

def test_history_empty(mock_db):
    mock_db_instance = mock_db.return_value
    mock_collection = MagicMock()
    mock_collection.find.return_value = []
    mock_db_instance.get_collection.return_value = mock_collection

    response = client.get("/model/history/")
    assert response.status_code == 200
    assert response.json()["history"] == []