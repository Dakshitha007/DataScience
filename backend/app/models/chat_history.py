from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)

    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)

    question = Column(Text, nullable=False)

    answer = Column(Text, nullable=False)

    case = relationship("Case", back_populates="chat_history")

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )