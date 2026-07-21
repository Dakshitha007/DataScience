from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class PoliceStation(Base):
    __tablename__ = "police_stations"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    station_code = Column(
        String(20),
        unique=True,
        nullable=False
    )

    station_name = Column(
        String(150),
        nullable=False
    )

    district = Column(
        String(100),
        nullable=False
    )

    city = Column(
        String(100),
        nullable=False
    )

    address = Column(
        String(255)
    )

    phone = Column(
        String(20)
    )

    latitude = Column(
        Float
    )

    longitude = Column(
        Float
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

    officers = relationship(
        "Officer",
        back_populates="police_station",
        cascade="all, delete-orphan"
    )

    cases = relationship(
        "Case",
        back_populates="police_station",
        cascade="all, delete-orphan"
    )