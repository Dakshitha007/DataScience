from pydantic import BaseModel, ConfigDict
from datetime import datetime


class CrimeBase(BaseModel):
    case_id: int
    crime_type: str
    location: str
    crime_date: datetime
    description: str


class CrimeCreate(CrimeBase):
    pass


class CrimeResponse(CrimeBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)