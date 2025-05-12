import os
import pickle
from fastapi import UploadFile, HTTPException

MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "airport_delay.pkl")
os.makedirs(MODEL_DIR, exist_ok=True)

class ModelLoader:
    def __init__(self):
        self.model = self.load_from_disk()

    def load_from_disk(self):
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, "rb") as f:
                return pickle.load(f)
        return None

    async def load(self, file: UploadFile):
        if not file.filename.endswith(".pkl"):
            raise HTTPException(status_code=400, detail="The file must be a .pkl template")

        contents = await file.read()
        with open(MODEL_PATH, "wb") as f:
            f.write(contents)
        self.model = pickle.loads(contents)
        return {"status": "Model loaded successfully", "filename": file.filename}
