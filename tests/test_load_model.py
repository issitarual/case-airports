from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_load_model_success():
    with open("src\\models\\airport_delay.pkl", "rb") as f:
        response = client.post("/model/load/", files={"file": ("model.pkl", f, "application/octet-stream")})

    assert response.status_code == 200
    assert response.json() == {"status": "Model loaded successfully", "filename": "model.pkl"}

def test_load_model_no_file():
    response = client.post("/model/load/")

    assert response.status_code == 422

def test_load_model_invalid_file_extension():
    with open("src\\models\\invalid_file.txt", "w") as f:
        f.write("This is not a .pkl file.")

    with open("src\\models\\invalid_file.txt", "rb") as f:
        response = client.post("/model/load/", files={"file": ("invalid_file.txt", f, "application/octet-stream")})

    assert response.status_code == 400
    assert response.json() == {"detail": "The file must be a .pkl template"}
