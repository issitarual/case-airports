from fastapi import FastAPI
from controllers import user, flight, health
import uvicorn

app = FastAPI()

app.include_router(flight.router, prefix="/model", tags=["model"])
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(health.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")