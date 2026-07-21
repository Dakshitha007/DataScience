from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class EvidenceFile(Base):
    __tablename__ = "evidence_files"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    evidence_id = Column(
        Integer,
        ForeignKey("evidence.id", ondelete="CASCADE"),
        nullable=False
    )

    file_name = Column(
        String(255),
        nullable=False
    )

    original_name = Column(
        String(255),
        nullable=False
    )

    file_path = Column(
        String(500),
        nullable=False
    )

    file_type = Column(
        String(50),
        nullable=False
    )

    file_size = Column(
        Integer,
        nullable=False
    )

    uploaded_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    uploaded_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    evidence = relationship(
        "Evidence",
        back_populates="files"
    )