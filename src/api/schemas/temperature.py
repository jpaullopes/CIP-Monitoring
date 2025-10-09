from pydantic import BaseModel
from datetime import datetime

class SensorDataPayload(BaseModel):
    temperature: float
    concentration: float
    flow: float

class SensorDataResponse(BaseModel):
    temperature: float
    concentration: float
    flow: float
    timestamp: datetime
    cip_id: int
    active: bool
