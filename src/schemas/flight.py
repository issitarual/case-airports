from pydantic import BaseModel
from datetime import datetime

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
    time_hour: datetime
