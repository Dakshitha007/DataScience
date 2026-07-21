from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.utils.enums import OfficerRank, OfficerStatus


class OfficerBase(BaseModel):
    user_id: int
    police_station_id: int
    badge_number: str
    first_name: str
    last_name: str
    rank: OfficerRank
    phone: str


class OfficerCreate(OfficerBase):
    pass


class OfficerUpdate(BaseModel):
    police_station_id: Optional[int] = None
    badge_number: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    rank: Optional[OfficerRank] = None
    phone: Optional[str] = None
    status: Optional[OfficerStatus] = None


class OfficerResponse(OfficerBase):
    id: int
    status: OfficerStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)