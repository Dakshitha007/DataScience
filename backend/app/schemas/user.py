from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.utils.enums import AppRole


class UserBase(BaseModel):
    email: str
    role: AppRole


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)