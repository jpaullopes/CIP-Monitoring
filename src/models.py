# models.py
from pydantic import BaseModel
from typing import Optional
from datetime import date as date_type, time as time_type

# --- Pydantic Models ---
class TemperatureReadingPayload(BaseModel):
    temperature: float
    humidity: float  # CAMPO OBRIGATÓRIO: Umidade
    pressure: float  # CAMPO OBRIGATÓRIO: Pressão
    sensor_id: str

class TemperatureDataResponse(BaseModel):
    id: Optional[str] = None  # InfluxDB doesn't use integer IDs like SQL
    temperature: float
    humidity: float  # CAMPO OBRIGATÓRIO: Umidade
    pressure: float  # CAMPO OBRIGATÓRIO: Pressão
    date_recorded: date_type
    time_recorded: time_type
    sensor_id: str
    client_ip: Optional[str] = None

    class Config:
        from_attributes = True
