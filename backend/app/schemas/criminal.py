from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


# ----------------------------
# Base Schema
# ----------------------------

class CriminalBase(BaseModel):
    criminal_code: str
    full_name: str
    alias: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    nationality: Optional[str] = "Indian"
    status: Optional[str] = "Active"


# ----------------------------
# Create
# ----------------------------

class CriminalCreate(CriminalBase):
    pass


# ----------------------------
# Update
# ----------------------------

class CriminalUpdate(BaseModel):
    criminal_code: Optional[str] = None
    full_name: Optional[str] = None
    alias: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    nationality: Optional[str] = None
    status: Optional[str] = None


# ----------------------------
# Summary
# ----------------------------

class CriminalSummaryResponse(BaseModel):
    id: int
    criminal_code: str
    full_name: str
    alias: Optional[str]
    gender: Optional[str]
    city: Optional[str]
    district: Optional[str]
    status: str

    model_config = ConfigDict(from_attributes=True)


# ----------------------------
# Response
# ----------------------------

class CriminalResponse(CriminalBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ----------------------------
# List Response
# ----------------------------

class CriminalListResponse(BaseModel):
    criminals: List[CriminalSummaryResponse]


# ----------------------------
# Dashboard
# ----------------------------

class CriminalDashboardResponse(BaseModel):
    total_criminals: int
    active: int
    arrested: int
    wanted: int
    released: int
    deceased: int


# ----------------------------
# Statistics
# ----------------------------

class CriminalStatisticsResponse(BaseModel):
    total_criminals: int
    male: int
    female: int
    other_gender: int
    indian: int
    foreign: int