from fastapi import APIRouter, UploadFile, File, HTTPException
from schemas.flight import FlightData
from services.flight import FlightService

router = APIRouter()
flight_service = FlightService()

@router.post("/load/")
async def load_model(file: UploadFile = File(...)):
    return await flight_service.load_model(file)

@router.post("/predict/")
async def predict(data: FlightData):
    return await flight_service.predict(data)

@router.get("/history/")
async def history():
    return flight_service.get_history()