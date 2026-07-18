from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CaseBase(BaseModel):
    case_number: str
    title: str
    description: str
    status: str
    priority: str
    station: str
    officer_id: int


class CaseCreate(CaseBase):
    pass


class CaseUpdate(BaseModel):
    case_number: str | None = None
    title: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None
    station: str | None = None
    officer_id: int | None = None


class CaseResponse(CaseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )