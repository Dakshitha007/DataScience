from pydantic import BaseModel, ConfigDict
from datetime import datetime


class VictimBase(BaseModel):
    case_id: int
    name: str
    age: int
    gender: str
    address: str
    phone: str


class VictimCreate(VictimBase):
    pass


class VictimResponse(VictimBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)