from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Enum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.base import Base
from app.utils.enums import CaseStatus, CasePriority

class Case(Base):
    __tablename__ = "cases"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    case_number = Column(
        String(50),
        unique=True,
        nullable=False,
    )

    fir_number = Column(
        String(50),
        unique=True,
        nullable=False,
    )

    crime_type = Column(
        String(100),
        nullable=False,
    )

    title = Column(
        String(200),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=False,
    )

    status = Column(
    Enum(CaseStatus),
    nullable=False,
    )

    priority = Column(
    Enum(CasePriority),
    nullable=False,
    )

    police_station_id = Column(
        Integer,
        ForeignKey("police_stations.id"),
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships

    police_station = relationship(
        "PoliceStation",
        back_populates="cases",
    )

    case_assignments = relationship(
        "CaseAssignment",
        back_populates="case",
        cascade="all, delete-orphan",
    )

    criminals = relationship(
        "CaseCriminal",
        back_populates="case",
        cascade="all, delete-orphan",
    )

    evidence = relationship(
        "Evidence",
        back_populates="case",
        cascade="all, delete-orphan",
    )

    activities = relationship(
        "CaseActivity",
        back_populates="case",
        cascade="all, delete-orphan",
    )