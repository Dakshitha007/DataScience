from sqlalchemy import Column, Integer, String, Date, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class Criminal(Base):
    __tablename__ = "criminals"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    criminal_code = Column(
        String(30),
        unique=True,
        nullable=False
    )

    full_name = Column(
        String(150),
        nullable=False
    )

    alias = Column(
        String(100)
    )

    gender = Column(
        String(20)
    )

    date_of_birth = Column(
        Date
    )

    phone = Column(
        String(20)
    )

    address = Column(
        Text
    )

    city = Column(
        String(100)
    )

    district = Column(
        String(100)
    )

    nationality = Column(
        String(50),
        default="Indian"
    )

    status = Column(
        String(30),
        default="Active"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    cases = relationship(
        "CaseCriminal",
        back_populates="criminal",
        cascade="all, delete-orphan"
    )

    outgoing_relations = relationship(
        "CriminalRelation",
        foreign_keys="CriminalRelation.criminal_id",
        back_populates="criminal",
        cascade="all, delete-orphan"
    )

    incoming_relations = relationship(
        "CriminalRelation",
        foreign_keys="CriminalRelation.related_criminal_id",
        back_populates="related_criminal",
        cascade="all, delete-orphan"
    )