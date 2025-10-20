from pydantic import BaseModel, Field
from datetime import datetime


class SensorDataPayload(BaseModel):
    temperature: float = Field(..., description="Temperature in celsius")
    concentration: float = Field(..., description="Concentration level")
    flow: float = Field(..., description="Flow rate")


class SensorDataResponse(BaseModel):
    temperature: float
    concentration: float
    flow: float
    timestamp: datetime
    cip_id: int
    active: bool
