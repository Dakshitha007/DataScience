from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CaseBase(BaseModel):
    case_number: str
    title: str
    description: str
    status: str
    priority: str
    officer_id: int


class CaseCreate(CaseBase):
    pass


class CaseUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None


class CaseResponse(CaseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)