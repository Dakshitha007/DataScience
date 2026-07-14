from pydantic import BaseModel, ConfigDict
from datetime import datetime


class SuspectBase(BaseModel):
    case_id: int
    name: str
    age: int
    gender: str
    status: str
    criminal_history: str | None = None


class SuspectCreate(SuspectBase):
    pass


class SuspectResponse(SuspectBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)