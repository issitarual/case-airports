from fastapi import FastAPI, UploadFile, File, HTTPException
from database import InMemoryDatabase
from pydantic import BaseModel
import pickle
import os
import numpy as np
import uvicorn

app = FastAPI()

MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "airport_delay.pkl")
os.makedirs(MODEL_DIR, exist_ok=True)
model = None
if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

class FlightData(BaseModel):
    year: int
    month: int
    day: int
    dep_time: float
    sched_dep_time: float
    dep_delay: float
    carrier: str
    flight: int
    origin: str
    dest: str
    air_time: float
    distance: float
    hour: int
    minute: int

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

@app.get("/health", status_code=200, tags=["health"], summary="Health check")
async def health():
    return {"status": "ok", "message": "API is working normally."}

@app.get("/model/history/", status_code=200, tags=["model"], summary="Forecast of delay at destination")
async def history():
    db = InMemoryDatabase()
    predictions = db.get_collection("predictions")
    return {"history": [x for x in predictions.find({}, {"_id": 0})]}

@app.post("/model/load/", status_code=200, tags=["model"], summary="Predict")
async def load_model(file: UploadFile = File(...)):
    global model

    if not file.filename.endswith(".pkl"):
        return {"error": "The file must be a .pkl template"}

    contents = await file.read()

    # Salva o modelo no disco
    with open(MODEL_PATH, "wb") as f:
        f.write(contents)

    # Recarrega o modelo na memória
    model = pickle.loads(contents)

    return {"status": "Model loaded successfully", "filename": file.filename}

@app.post("/model/predict/", status_code=200, tags=["model"], summary="Prediction history")
async def predict(data: FlightData):
    global model
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Use /model/load/")

    input_features = np.array([[
            data.year,
            data.month,
            data.day,
            data.dep_time,
            data.sched_dep_time,
            data.dep_delay,
            data.carrier,
            data.flight,
            data.origin,
            data.dest,
            data.air_time,
            data.distance,
            data.hour,
            data.minute,
        ]])

    try:
        prediction = float(model.predict(input_features)[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao prever: {str(e)}")

    db = InMemoryDatabase()
    predictions = db.get_collection("predictions")
    predictions.insert_one({**data.dict(), "prediction": prediction})

    return {"prediction": prediction}

@app.post("/user/", tags=["example"], summary="Insert user")
async def insert(data: dict):
    db = InMemoryDatabase()
    users = db.get_collection('users')
    users.insert_one(data)
    return {"status": "ok"}

@app.get("/user/{name}", status_code=200, tags=["example"], summary="Get user by name")
async def get(name: str):
    db = InMemoryDatabase()
    users = db.get_collection('users')
    user = users.find_one({"name": name})
    return {"status": "ok", "user": user}

@app.get("/user/", tags=["example"], summary="List all users")
async def list():
    db = InMemoryDatabase()
    users = db.get_collection('users')
    return {"status": "ok", "users": [x for x in users.find({},{"_id": 0})]}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")