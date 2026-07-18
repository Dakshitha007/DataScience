from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class Officer(Base):
    __tablename__ = "officers"

    id = Column(Integer, primary_key=True, index=True)

    # Link Officer to User
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    badge_number = Column(
        String(50),
        unique=True,
        nullable=False
    )

    name = Column(
        String(100),
        nullable=False
    )

    designation = Column(
        String(50),
        nullable=False
    )

    station = Column(
        String(100),
        nullable=False
    )

    phone = Column(
        String(20),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # One-to-One Relationship with User
    user = relationship(
        "User",
        back_populates="officer"
    )

    # One-to-Many Relationship with Cases
    cases = relationship(
        "Case",
        back_populates="officer"
    )