from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.utils.enums import CasePriority, CaseStatus


class CaseBase(BaseModel):
    case_number: str
    fir_number: str
    crime_type: str
    title: str
    description: str
    status: CaseStatus
    priority: CasePriority
    police_station_id: int


class CaseCreate(BaseModel):
    case_number: str
    fir_number: str
    crime_type: str
    title: str
    description: str
    status: CaseStatus
    priority: CasePriority
    police_station_id: int


class CaseUpdate(BaseModel):
    case_number: Optional[str] = None
    fir_number: Optional[str] = None
    crime_type: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[CaseStatus] = None
    priority: Optional[CasePriority] = None
    police_station_id: Optional[int] = None


class CaseResponse(CaseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)