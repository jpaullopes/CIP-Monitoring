from pydantic import BaseModel
from datetime import date as date_type, time as time_type
from typing import Optional

class TemperatureReadingPayload(BaseModel):
    temperature: float
    humidity: float
    pressure: float
    sensor_id: str

class TemperatureDataResponse(BaseModel):
    id: Optional[str] = None
    temperature: float
    humidity: float
    pressure: float
    date_recorded: date_type
    time_recorded: time_type
    sensor_id: str
    client_ip: Optional[str] = None
