from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ChatHistoryBase(BaseModel):
    case_id: int
    question: str
    answer: str


class ChatHistoryCreate(ChatHistoryBase):
    pass


class ChatHistoryResponse(ChatHistoryBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)