from pydantic import BaseModel, ConfigDict
from datetime import datetime


class EvidenceBase(BaseModel):
    case_id: int
    evidence_type: str
    description: str
    file_path: str | None = None


class EvidenceCreate(EvidenceBase):
    pass


class EvidenceResponse(EvidenceBase):
    id: int
    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)