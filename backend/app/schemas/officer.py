from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.utils.enums import Designation


class OfficerBase(BaseModel):
    user_id: int
    badge_number: str
    name: str
    designation: Designation
    station: str
    phone: str


class OfficerCreate(OfficerBase):
    pass


class OfficerResponse(OfficerBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)