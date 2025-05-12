from fastapi import UploadFile, File, HTTPException
from repositories.flight import FlightRepository
from schemas.flight import FlightData
from core.model_loader import ModelLoader
import numpy as np

class FlightService:
    def __init__(self):
        self.model_loader = ModelLoader()
        self.repo = FlightRepository()

    async def load_model(self, file: UploadFile):
        return await self.model_loader.load(file)

    async def predict(self, data: FlightData):
        model = self.model_loader.model
        if not model:
            raise HTTPException(status_code=503, detail="Model not loaded.")

        input_features = np.array([[
            data.year, data.month, data.day, data.dep_time,
            data.sched_dep_time, data.dep_delay, data.carrier,
            data.flight, data.origin, data.dest, data.air_time,
            data.distance, data.hour, data.minute
        ]])

        try:
            prediction = float(model.predict(input_features)[0])
            self.repo.save_prediction(data.dict(), prediction)
            return {"prediction": prediction}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao prever: {str(e)}")

    def get_history(self):
        return self.repo.get_all_predictions()
