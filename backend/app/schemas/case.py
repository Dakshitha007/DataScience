from pydantic import BaseModel, ConfigDict
from datetime import datetime


class CaseBase(BaseModel):
    case_number: str
    title: str
    description: str
    status: str
    priority: str
    officer_id: int


class CaseCreate(CaseBase):
    pass


class CaseResponse(CaseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)