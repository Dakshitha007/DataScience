from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class AIReport(Base):
    __tablename__ = "ai_reports"

    id = Column(Integer, primary_key=True, index=True)

    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)

    summary = Column(Text, nullable=False)

    crime_pattern = Column(Text, nullable=True)

    risk_level = Column(String(20), nullable=False)

    recommendations = Column(Text, nullable=True)

    case = relationship("Case", back_populates="ai_reports")

    generated_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )