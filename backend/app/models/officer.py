from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class Officer(Base):
    __tablename__ = "officers"

    id = Column(Integer, primary_key=True, index=True)

    badge_number = Column(String(50), unique=True, nullable=False)

    name = Column(String(100), nullable=False)

    rank = Column(String(50), nullable=False)

    station = Column(String(100), nullable=False)

    phone = Column(String(20), nullable=False)

    email = Column(String(150), unique=True, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    cases = relationship("Case", back_populates="officer")