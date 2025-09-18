from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SensorDataPayload(BaseModel):
    pressure: float
    temperature: float
    concentration: float
    flow: float

class SensorDataResponse(BaseModel):
    pressure: float
    temperature: float
    concentration: float
    flow: float
    timestamp: datetime
    cip_id: int
