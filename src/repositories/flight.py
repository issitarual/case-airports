from database import InMemoryDatabase

class FlightRepository:
    def __init__(self):
        self.db = InMemoryDatabase()
        self.collection = self.db.get_collection("predictions")

    def save_prediction(self, data: dict, prediction: float):
        self.collection.insert_one({**data, "prediction": prediction})

    def get_all_predictions(self):
        return {"history": [x for x in self.collection.find({}, {"_id": 0})]}
