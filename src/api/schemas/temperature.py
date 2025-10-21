from pydantic import BaseModel, Field
from datetime import datetime


class SensorDataPayload(BaseModel):
    temperature: float = Field(..., description="Temperature in celsius")
    conductivity: float = Field(..., description="Conductivity level")
    flow: float = Field(..., description="Flow rate")


class SensorDataResponse(BaseModel):
    temperature: float
    conductivity: float
    flow: float
    timestamp: datetime
    cip_id: int
    active: bool
