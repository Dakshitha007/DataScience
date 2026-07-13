from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)

    case_number = Column(String(50), unique=True, nullable=False)

    title = Column(String(200), nullable=False)

    description = Column(Text, nullable=False)

    status = Column(String(50), nullable=False)

    priority = Column(String(20), nullable=False)

    officer_id = Column(Integer, ForeignKey("officers.id"), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # Relationships
    officer = relationship("Officer", back_populates="cases")

    crimes = relationship("Crime", back_populates="case")

    victims = relationship("Victim", back_populates="case")

    suspects = relationship("Suspect", back_populates="case")

    evidence = relationship("Evidence", back_populates="case")

    chat_history = relationship("ChatHistory", back_populates="case")

    ai_reports = relationship("AIReport", back_populates="case")

    predictions = relationship("Prediction", back_populates="case")