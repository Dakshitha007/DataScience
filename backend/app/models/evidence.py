from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(Integer, primary_key=True, index=True)

    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)

    evidence_type = Column(String(50), nullable=False)

    description = Column(Text, nullable=False)

    file_path = Column(String(255), nullable=True)

    case = relationship("Case", back_populates="evidence")

    uploaded_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )