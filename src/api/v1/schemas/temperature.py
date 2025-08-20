from pydantic import BaseModel
from datetime import date as date_type, time as time_type
from typing import Optional

class TemperatureReadingPayload(BaseModel):
    id_sensor: str
    cip_id: str
    status_cip: str
    temperature: float
    pressure: float
    concentration: float

#{'id_sensor': 'estacao_cip', 'cip_id': '1', 'status_cip': 'true', 'temperature': 20.81, 'pressure': 1.42, 'concentration': 0.01}


class CipDataResponse(BaseModel):
    id: Optional[str] = None
    temperature: float
    pressure: float
    concentration: float
    date_recorded: date_type
    time_recorded: time_type
    id_sensor: str
    cip_id: str
    status_cip: str
    client_ip: Optional[str] = None

class TemperatureDataResponse(BaseModel):
    id: Optional[str] = None
    temperature: float
    humidity: float
    pressure: float
    date_recorded: date_type
    time_recorded: time_type
    sensor_id: str
    client_ip: Optional[str] = None
