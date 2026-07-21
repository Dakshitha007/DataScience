from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PoliceStationBase(BaseModel):
    station_code: str
    station_name: str
    district: str
    city: str
    address: Optional[str] = None
    phone: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class PoliceStationCreate(PoliceStationBase):
    pass


class PoliceStationUpdate(BaseModel):
    station_code: Optional[str] = None
    station_name: Optional[str] = None
    district: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class PoliceStationResponse(PoliceStationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)