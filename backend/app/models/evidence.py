from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    case_id = Column(
        Integer,
        ForeignKey(
            "cases.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    title = Column(
        String(255),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    evidence_type = Column(
        String(50),
        nullable=False,
    )

    location_found = Column(
        String(255),
        nullable=True,
    )

    collected_by = Column(
        String(255),
        nullable=False,
    )

    collection_date = Column(
        DateTime(timezone=True),
        nullable=False,
    )

    storage_location = Column(
        String(255),
        nullable=True,
    )

    status = Column(
        String(50),
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

    case = relationship(
        "Case",
        back_populates="evidences",
    )