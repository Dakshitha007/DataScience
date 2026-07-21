from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base
from app.utils.enums import (
    OfficerRank,
    OfficerStatus,
)


class Officer(Base):
    __tablename__ = "officers"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    police_station_id = Column(
        Integer,
        ForeignKey("police_stations.id"),
        nullable=False
    )

    badge_number = Column(
        String(50),
        unique=True,
        nullable=False
    )

    first_name = Column(
        String(50),
        nullable=False
    )

    last_name = Column(
        String(50),
        nullable=False
    )

    rank = Column(
        Enum(OfficerRank),
        nullable=False
    )

    phone = Column(
        String(20),
        nullable=False
    )

    status = Column(
        Enum(OfficerStatus),
        nullable=False,
        default=OfficerStatus.ACTIVE,
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

    # Relationships

    user = relationship(
        "User",
        back_populates="officer"
    )

    police_station = relationship(
        "PoliceStation",
        back_populates="officers"
    )

    case_assignments = relationship(
        "CaseAssignment",
        back_populates="officer",
        cascade="all, delete-orphan"
    )