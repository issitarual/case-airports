from fastapi import HTTPException
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.main import app
from src.schemas.flight import FlightData
from src.services.flight import FlightService

client = TestClient(app)

class MockModel:
    def predict(self, X):
        return [42.0]

valid_input = {
    "year": 2024,
    "month": 5,
    "day": 12,
    "dep_time": 1230.0,
    "sched_dep_time": 1200.0,
    "dep_delay": 30.0,
    "carrier": "AA",
    "flight": 100,
    "origin": "JFK",
    "dest": "LAX",
    "air_time": 300.0,
    "distance": 2500.0,
    "hour": 12,
    "minute": 30,
    "time_hour": "2024-05-12T12:00:00"
}

@pytest.fixture
def mock_model():
    with patch("src.main.model", new=MockModel()):
        yield

@pytest.mark.asyncio
async def test_predict():
    data = FlightData(
        year=2024,
        month=5,
        day=12,
        dep_time=100.0,
        sched_dep_time=950,
        dep_delay=10.2,
        carrier='UA',
        flight=1234,
        origin='EWR',
        dest='IAH',
        air_time=150.3,
        distance=1000,
        hour=10,
        minute=0,
        time_hour="2024-05-12T12:00:00"
    )

    mock_model = MagicMock()
    mock_model.predict.return_value = [42.0]

    with patch("src.services.flight.ModelLoader") as MockModelLoader, \
         patch("src.services.flight.FlightRepository") as MockRepository:

        mock_loader_instance = MockModelLoader.return_value
        mock_loader_instance.model = mock_model

        mock_repo_instance = MockRepository.return_value
        mock_repo_instance.save_prediction = MagicMock()

        service = FlightService()
        result = await service.predict(data)

        assert result == {"prediction": 42.0}
        mock_model.predict.assert_called_once()
        mock_repo_instance.save_prediction.assert_called_once()

@pytest.mark.asyncio
async def test_predict_without_model():
    data = FlightData(**valid_input)

    with patch("src.services.flight.ModelLoader") as MockModelLoader:
        mock_loader_instance = MockModelLoader.return_value
        mock_loader_instance.model = None

        service = FlightService()

        with pytest.raises(HTTPException) as excinfo:
            await service.predict(data)

        assert excinfo.value.status_code == 503
        assert "Model not loaded" in str(excinfo.value.detail)

def test_predict_missing_feature():
    incomplete_input = valid_input.copy()
    del incomplete_input["carrier"]

    response = client.post("/model/predict/", json=incomplete_input)
    assert response.status_code == 422

def test_predict_no_body():
    response = client.post("/model/predict/")
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_predict_model_fails():
    data = FlightData(**valid_input)

    failing_model = MagicMock()
    failing_model.predict.side_effect = Exception("Falha na predição")

    with patch("src.services.flight.ModelLoader") as MockModelLoader, \
         patch("src.services.flight.FlightRepository") as MockRepository:

        mock_loader_instance = MockModelLoader.return_value
        mock_loader_instance.model = failing_model

        mock_repo_instance = MockRepository.return_value

        service = FlightService()

        with pytest.raises(HTTPException) as excinfo:
            await service.predict(data)

        assert excinfo.value.status_code == 404
        assert "Error in prediction:" in str(excinfo.value.detail)