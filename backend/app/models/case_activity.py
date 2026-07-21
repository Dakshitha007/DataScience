from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class CaseActivity(Base):
    __tablename__ = "case_activities"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    case_id = Column(
        Integer,
        ForeignKey("cases.id", ondelete="CASCADE"),
        nullable=False
    )

    officer_id = Column(
        Integer,
        ForeignKey("officers.id"),
        nullable=True
    )

    activity_type = Column(
        String(100),
        nullable=False
    )

    description = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    case = relationship(
        "Case",
        back_populates="activities"
    )

    officer = relationship(
        "Officer"
    )