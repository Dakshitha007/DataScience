from pydantic import BaseModel, ConfigDict
from datetime import datetime


class AIReportBase(BaseModel):
    case_id: int
    summary: str
    crime_pattern: str | None = None
    risk_level: str
    recommendations: str | None = None


class AIReportCreate(AIReportBase):
    pass


class AIReportResponse(AIReportBase):
    id: int
    generated_at: datetime

    model_config = ConfigDict(from_attributes=True)