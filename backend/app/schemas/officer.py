from pydantic import BaseModel, ConfigDict
from datetime import datetime


class OfficerBase(BaseModel):
    badge_number: str
    name: str
    rank: str
    station: str
    phone: str
    email: str


class OfficerCreate(OfficerBase):
    pass


class OfficerResponse(OfficerBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)