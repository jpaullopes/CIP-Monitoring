# models.py
from sqlalchemy import Column, Integer, String, Float, Date, Time
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Optional
from datetime import date as date_type, time as time_type

# SQLAlchemy Base
Base = declarative_base()

# --- SQLAlchemy Models (Database Tables) ---
class DataDB(Base):
    __tablename__ = "data"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    pressure = Column(Float, nullable=False)
    date_recorded = Column(Date, nullable=False, index=True)
    time_recorded = Column(Time, nullable=False, index=True)
    sensor_id = Column(String, nullable=False, index=True)
    client_ip = Column(String, nullable=True)

# --- Pydantic Models ---
class TemperatureReadingPayload(BaseModel):
    temperature: float
    humidity: float  # CAMPO OBRIGATÓRIO: Umidade
    pressure: float  # CAMPO OBRIGATÓRIO: Pressão
    sensor_id: str

class TemperatureDataResponse(BaseModel):
    id: Optional[int] = None
    temperature: float
    humidity: float  # CAMPO OBRIGATÓRIO: Umidade
    pressure: float  # CAMPO OBRIGATÓRIO: Pressão
    date_recorded: date_type
    time_recorded: time_type
    sensor_id: str
    client_ip: Optional[str] = None

    class Config:
        from_attributes = True
