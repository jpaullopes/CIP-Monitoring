from pydantic import BaseModel
from datetime import date as date_type, time as time_type
from typing import Optional

class CipMonitoringPayload(BaseModel):
    temperature: float
    pressure: float
    concentration: float
    id_sensor: str
    cip_id: str
    status_cip: str

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
