from pydantic import BaseModel, ConfigDict
from datetime import datetime


class PredictionBase(BaseModel):
    case_id: int
    prediction: str
    confidence: float


class PredictionCreate(PredictionBase):
    pass


class PredictionResponse(PredictionBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)